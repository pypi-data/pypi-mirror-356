import numpy as np
import time
import threading
import socket
import json
import atexit
import logging

from torch.cuda.amp import autocast
from nxva.v11 import Detector
from nxva.streaming import MultiStreaming
from collections import deque, defaultdict
from multiprocessing import shared_memory, Lock

logger = logging.getLogger('mlt')

class DetectionServer:
    def __init__(self, max_detection_num, model_list, task_class_names, all_cameras_ids, lock_dict):
        '''
        Args:
            max_detection_num: int
                max number of detection in a frame
            model_list: list
                list of model names
                model_list = ['./config/detection.yaml', ...]
            task_class_names: list
                list of class names which the task needs
                task_class_names = ['people', 'car', ...]
            all_cameras_ids: list
                append all cameras.yaml where in cameras's folder
            lock_dict: dict
                lock_dict[lock_number] = Lock()

        Attributes:
            max_detection_num: int
                max number of detection in a frame
            lock_dict: dict
                lock_dict[lock_number] = Lock()
            all_cameras_ids: list
                append all cameras.yaml where in cameras's folder
            sock: socket.socket
                socket
            stream: MultiStreaming
                streaming
            detector: DetectorBuilder
                detector
            model_dict: dict
                run models by model_name
                model_dict[model_name] = model
            class_name_dict: dict
                send class names to client after label shift
                class_name_dict = {0: 'people', ...}
            label_shift: dict
                label shift
                label_shift[model_name] = shift
            task_class_list: dict
                choose results which the task needs from merged_results
                task_class_list[register_name] = [class_id1, class_id2, ...]
            label_shift: dict
                merge all labels
                label_shift[model_name] = shift
            task_list: list
                list of task names
                task_list = [task1, task2, ...]
            camera_indices_dict: dict
                camera_indices_dict[register_name] = cameras_list
            name_class_dict: dict
                name_class_dict = {class_name: class_id, ...}
            shm_dict: dict
                shm_dict[register_name] = [frames_shm, results_shm]
            buffer_dict: dict
                buffer_dict[register_name] = [frames_buffer, results_buffer]
            task_queue_dict: dict
                task_queue_dict[register_name] = queue.Queue()
            queue_lock: threading.Lock

        '''
        self.max_detection_num     = max_detection_num
        self.lock_dict             = lock_dict

        self.all_cameras_ids       = all_cameras_ids

        # socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
        self.sock.bind(('127.0.0.1', 9453))
        atexit.register(self.sock.close)

        # streaming
        self.stream = MultiStreaming(config='./configs/streaming.yaml', 
                                    reconnect_interval=30,
                                    verbose=True
                                    )
        self.stream.init_cameras()
        self.stream.run()

        # model yaml
        self.model_dict       = {}
        self.class_name_dict  = {}
        self.label_shift      = {}
        shift                 = 0
        
        for model_name in model_list:
            model = Detector(f'{model_name}')
            class_names = model.class_names

            names_class = {name: class_id for class_id, name in class_names.items()}
            
            model_class_list = []
            for task_class_name in task_class_names:
                class_id = names_class.get(task_class_name)
                if class_id != None:
                    model_class_list.append(class_id)
            
            model.classes = model_class_list
            model.max_det = max_detection_num
            self.model_dict[model_name] = model

            # label shift
            for id, class_name in class_names.items():
                if class_name not in self.class_name_dict.values():
                    self.class_name_dict.update({id + shift: class_name})

            self.label_shift[model_name] = shift  
            shift += len(class_names)

        # reverse class_name_dict
        self.name_class_dict     = {name: class_id for class_id, name in self.class_name_dict.items()}
        
        # task
        self.task_list           = []

        # camera indices
        self.camera_indices_dict = {}

        # class_id
        self.task_class_list     = defaultdict(list)

        # shared memory
        self.shm_dict            = {}
        self.buffer_dict         = {}

        # queue
        self.task_queue_dict     = {}

        # lock
        self.queue_lock          = threading.Lock()

        threading.Thread(target=self._registration_server, daemon=True).start()
    
    def _registration_server(self):
        logger.info('Waiting for connection...')
        while True:
            data, addr = self.sock.recvfrom(1024)

            message       = json.loads(data.decode())
            register_name = message['task']
            cameras_ids   = message['camera_ids']
            class_name    = message['class_names']
            lock_number   = message['lock_number']
            frames_shm_name, results_shm_name, count_shared_name, frames_buffer_shape, results_buffer_shape, class_name_dict = self._register_task(cameras_ids, register_name, class_name, lock_number)
            respone = {
                'frames_shm_name': frames_shm_name,
                'results_shm_name': results_shm_name,
                'count_shared_name': count_shared_name,
                'frames_buffer_shape': frames_buffer_shape,
                'results_buffer_shape': results_buffer_shape,
                'class_name_dict': class_name_dict
            }
            self.sock.sendto(json.dumps(respone).encode(), addr)
            time.sleep(0.001)

    def _register_task(self, cameras_ids, register_name, class_names, lock_number):
        '''
        Register task.

        Args:
            cameras_ids: list
                cameras ids
            register_name: str
                register name
            class_names: list
                class names
            lock_number: str
                lock number
        
        Returns:
            frames_shm_name: str
                shared memory name of frames
            results_shm_name: str
                shared memory name of results
            frames_buffer_shape: tuple
                shape of frames buffer
            results_buffer_shape: tuple
                shape of results buffer
        '''
        frames_shm_name, results_shm_name, count_shared_name, frames_buffer_shape, results_buffer_shape = self._build_shared_memory(cameras_ids, register_name)
        # build queue
        self.task_queue_dict[register_name] = deque(maxlen=1)

        self.camera_indices_dict.update(self._build_camera_indices(self.all_cameras_ids, cameras_ids, register_name))
        threading.Thread(target=self._get_frames_results_queue, args=(register_name, self.lock_dict[lock_number],), daemon=True).start()

        # find class_id in class_names
        for class_name in class_names:
            class_id = self.name_class_dict.get(class_name)
            if class_id != None:
                self.task_class_list[register_name].append(class_id)
                
        # return class_names which task need
        class_name_dict = {class_id: self.class_name_dict[class_id] for class_id in self.task_class_list[register_name] if class_id in self.class_name_dict}

        self.task_list.append(register_name)
        logger.info(f"Register task: {self.task_list}")

        return frames_shm_name, results_shm_name, count_shared_name, frames_buffer_shape, results_buffer_shape, class_name_dict

    def _build_shared_memory(self, cameras_ids, register_name):
        '''
        Build shared memory for frames and results per task.

        Args:
            cameras_ids: list
                cameras ids
            register_name: str
                register name
        
        Returns:
            frames_shared_name: str
                shared memory name of frames
            results_shared_name: str
                shared memory name of results
            frames_buffer_shape: tuple
                shape of frames buffer
            results_buffer_shape: tuple
                shape of results buffer
        '''
        w = self.stream.w
        h = self.stream.h

        # SharedMemory
        MAX_ROWS = self.max_detection_num # 最大偵測數量
        MAX_COLS = 6 # results.shape

        cameras_num         = len(cameras_ids) # 攝影機數量
        frames_shared_name  = f"frames_{register_name}"

        self.shm_dict[register_name]    = []
        self.buffer_dict[register_name] = []

        # Build shared memory for frames and results per task
        # frames
        try:
            self.shm_dict[register_name].append(shared_memory.SharedMemory(name=frames_shared_name, create=True, size=w * h * 3 * cameras_num))  # 寬x高x通道x數量
        except FileExistsError:
            shared_memory.SharedMemory(name=frames_shared_name).close()
            shared_memory.SharedMemory(name=frames_shared_name).unlink()
            self.shm_dict[register_name].append(shared_memory.SharedMemory(name=frames_shared_name, create=True, size=w * h * 3 * cameras_num))

        self.buffer_dict[register_name].append(np.ndarray((cameras_num, h, w, 3), dtype=np.uint8, buffer=self.shm_dict[register_name][-1].buf))
        
        atexit.register(shared_memory.SharedMemory(name=frames_shared_name).close)
        atexit.register(shared_memory.SharedMemory(name=frames_shared_name).unlink)

        # results
        results_shared_name  = f"results_{register_name}"
        try:
            self.shm_dict[register_name].append(shared_memory.SharedMemory(name=results_shared_name, create=True, size=cameras_num * MAX_ROWS * MAX_COLS * np.float32().itemsize))
        except FileExistsError:
            shared_memory.SharedMemory(name=results_shared_name).close()
            shared_memory.SharedMemory(name=results_shared_name).unlink()
            self.shm_dict[register_name].append(shared_memory.SharedMemory(name=results_shared_name, create=True, size=cameras_num * MAX_ROWS * MAX_COLS * np.float32().itemsize))

        self.buffer_dict[register_name].append(np.ndarray((cameras_num, MAX_ROWS, MAX_COLS), dtype=np.float32, buffer=self.shm_dict[register_name][-1].buf))
        
        atexit.register(shared_memory.SharedMemory(name=results_shared_name).close)
        atexit.register(shared_memory.SharedMemory(name=results_shared_name).unlink)

        # count
        count_shared_name = f"count_{register_name}"
        try:
            self.shm_dict[register_name].append(shared_memory.SharedMemory(name=count_shared_name, create=True, size=np.array([0], dtype=np.int32).nbytes))
        except FileExistsError:
            self.shm_dict[register_name].append(shared_memory.SharedMemory(name=count_shared_name))

        self.buffer_dict[register_name].append(np.ndarray((1,), dtype=np.int32, buffer=self.shm_dict[register_name][-1].buf))
        
        return frames_shared_name, results_shared_name, count_shared_name, self.buffer_dict[register_name][0].shape, self.buffer_dict[register_name][1].shape
    
    def _build_camera_indices(self, all_cameras_ids, cameras_ids, register_name):
        '''
        Build camera indices per task.

        Args:
            cameras_ids: list
                camera ids
            register_name: str
                register name
        '''
        return {
            register_name: [
                all_cameras_ids.index(task_camera)
                for task_camera in cameras_ids if task_camera in all_cameras_ids
            ]
        }

    def _get_frames_results_queue(self, register_name, lock):
        '''
        If queue is not empty, get frames and results from queue, and put them into frames_buffer and results_buffer.
        self.buffer_dict[register_name] = [frames_buffer, results_buffer, count_buffer]
        self.queue_lock: threading.Lock

        Args:
            register_name: str
                register name
            lock: multiprocess.Lock
        '''
        count = 0
        while True:
            if len(self.task_queue_dict[register_name]) > 0:
                with self.queue_lock:
                    frames, results = self.task_queue_dict[register_name].popleft()
                
                results_buffer_list = []
                _, max_rows, max_cols  = self.buffer_dict[register_name][1].shape
                for result in results:
                    padded_result = np.full((max_rows, max_cols), -1, dtype=np.float32)  # padding
                    rows = min(result.shape[0], max_rows)
                    padded_result[:rows, :result.shape[1]] = result[:rows, :result.shape[1]]  # padding
                    results_buffer_list.append(padded_result)

                with lock:
                    self.buffer_dict[register_name][0][:] = frames
                    self.buffer_dict[register_name][1][:] = results_buffer_list
                    self.buffer_dict[register_name][2][0] = count
                    count += 1
                if count >= 1000:
                    count = 0
                    
            time.sleep(0.001)


    def run(self):
        '''
        Run get_frames_results_queue threading.
        Get frames and results from stream, and put them into queue.

        Args:
            event: threading.Event
        '''
        num_frames = self.stream.num

        while True:
            merged_results = [np.empty((0, 6), dtype=float) for _ in range(num_frames)]
            if len((self.task_list)) > 0:
                frames, status = self.stream.get_frames(status=True)

                for model_name, model in self.model_dict.items():
                    with autocast():
                        results = model(frames)

                    # Shift class_id and merge results
                    for frame_idx, result in enumerate(results):
                        if result.shape[1] >= 6:
                            result[:, 5] += self.label_shift[model_name]
                        merged_results[frame_idx % num_frames] = np.vstack((merged_results[frame_idx % num_frames], result))

                for register_name in self.task_list:
                    camera_images_list  = [frames[idx] for idx in self.camera_indices_dict[register_name]]
                    camera_results_list = [merged_results[idx] for idx in self.camera_indices_dict[register_name]]

                    filtered_results = [
                        result[np.isin(result[:, 5].astype(int), self.task_class_list[register_name])] if result.size > 0 else result
                        for result in camera_results_list
                    ]

                    with self.queue_lock:
                        self.task_queue_dict[register_name].append((camera_images_list, filtered_results))

            time.sleep(0.001)

if __name__ == "__main__":
    from utilities import load_configs

    task_list, hyper_config, streaming_config, cameras_dict, cameras_configs_dict, all_cameras_ids = load_configs()
    lock_dict = {task: Lock() for task in task_list}
    max_detection_num = hyper_config['shared_memory']['max_detection_num']
    model_list        = hyper_config['model']['model_list']
    class_names  = [config['class'] for _, config in hyper_config.items() if 'class' in config]
    task_class_names = list(set(name for class_name in class_names for name in class_name))

    dection_server = DetectionServer(max_detection_num, model_list, task_class_names, all_cameras_ids, lock_dict)
    dection_server.run()

    