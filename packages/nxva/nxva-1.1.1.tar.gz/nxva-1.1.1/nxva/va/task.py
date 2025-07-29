import cv2
import time
import json
import socket
import queue
import threading
import numpy as np

from nxva.streaming import MultiStreaming
from nxva.vision import images_automerge
from multiprocessing import shared_memory, current_process

class BaseTask:
    lock_dict = None
    def __init__(self, class_names, cameras_ids, interval=0, test_mode=False):
        '''
        Args:
            interval: float
                the interval of task
            class_names: list
                class names = [people]
            cameras_ids: list
                the task needs to be run on which cameras
            test_mode: bool
                if test_mode is True, the task will run in single process
        
        Attributes:
            register_name: str
                register name of task to detection server
                register_name = current_process().name
            lock_number: str
                lock number of task to choose lock_dict
            test_mode: bool
                if test_mode is True, the task will run in single process
            queue: queue.Queue
                queue
            queue_lock: threading.Lock
                queue lock
            class_name_dict: dict
                the labels after label shift
                class_name_dict = {0: 'people', ...}
        
        Methods:
            _register:
                send message to detection server with socket
            _get_results_from_shm:
                get results from shared memory and put them into queue
            run:
                use frames and results to process run_once and draw_images
            get_queue:
                get frames and results from queue
            run_once:
                need to implement in subclasses to run task
            draw_images:
                need to implement in subclasses to draw images
        '''
        self.interval = interval

        register_name = current_process().name
        lock_number   = str(register_name.split('-')[-1])

        self.test_mode = test_mode
        
        self.queue       = queue.Queue()
        self.queue_lock  = threading.Lock()
        self.stop_event  = threading.Event()

        if not self.test_mode:
            shm_info = self._register(register_name, cameras_ids, class_names, lock_number)
            self.class_name_dict = shm_info['class_name_dict']
            threading.Thread(
                target=self._get_results_from_shm, 
                args=(
                    shm_info['frames_shm_name'], 
                    shm_info['frames_buffer_shape'], 
                    shm_info['results_shm_name'], 
                    shm_info['results_buffer_shape'],
                    shm_info['count_shared_name'],
                    BaseTask.lock_dict[lock_number],
                ), 
                daemon=True
            ).start()

    def _register(self, register_name, camera_ids, class_names, lock_number):
        """
        Register task to detection server
        
        Args:
            register_name: str
                register name of task to detection server
            camera_ids: list
                the task needs to be run on which cameras
                camera_ids = ['IPCAM-201', 'IPCAM-206']
            class_names: list
                class names = [people]
            lock_number: str
                lock number of task to choose lock_dict
                
        Returns:
            shm_info: dict
                shared memory info
                {'frames_shm_name': 'frames_shm_name', 'frames_buffer_shape': (1080, 1920, 3), 'results_shm_name': 'results_shm_name', 'results_buffer_shape': (15, 6), 'class_name_dict': {0: 'people', ...}}
        """
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            message = {
                'task'          : register_name,
                'camera_ids'    : camera_ids,
                'class_names'   : class_names,
                'lock_number'   : lock_number
            }
            message_json = json.dumps(message)

            sock.sendto(message_json.encode(), ('127.0.0.1', 9453))
            data = sock.recv(3072).decode() # the buffer size
            shm_info = json.loads(data)

        return shm_info

    def _get_results_from_shm(self, frames_shm_name, frames_shape, results_shm_name, results_shape, count_shared_name, shm_lock):
        """
        Get results from shared memory and put them into queue
        
        Args:
            frames_shm_name: str
                shared memory name of frames
            frames_shape: tuple
                shape of frames
                frames_shape = (1080, 1920, 3)
            results_shm_name: str
                shared memory name of results
            results_shape: tuple
                shape of results
                results_shape = (15, 6)
            shm_lock: mutilprocess.Lock
                lock_dict[lock_number]
        """
        # SharedMemory
        frames_shm  = shared_memory.SharedMemory(name=frames_shm_name)
        results_shm = shared_memory.SharedMemory(name=results_shm_name)
        count_shm   = shared_memory.SharedMemory(name=count_shared_name)

        frames_buffer  = np.ndarray(frames_shape, dtype=np.uint8, buffer=frames_shm.buf)
        results_buffer = np.ndarray(results_shape, dtype=np.float32, buffer=results_shm.buf)
        count_buffer   = np.ndarray((1,), dtype=np.int32, buffer=count_shm.buf)

        frames_list  = np.ndarray(frames_shape, dtype=np.uint8)
        results_list = np.ndarray(results_shape, dtype=np.float32)
        count_list   = np.ndarray((1,), dtype=np.int32)

        while True:
            with shm_lock:
                # check if the count is the same
                if count_list[:] == count_buffer[:]:
                    time.sleep(0.001)
                    continue

                frames_list[:]  = frames_buffer[:]
                results_list[:] = results_buffer[:]
                count_list[:]   = count_buffer[:]

            with self.queue_lock:
                self.queue.put((frames_list, results_list))
            time.sleep(0.001)

    def run(self, show=True):
        """
        Use frames and results to process run_once and draw_images
        
        Args:
            show: bool
                if show is True, show images
        """
        next_time = time.perf_counter() + self.interval
        if show:
            cv2.namedWindow('show', cv2.WINDOW_NORMAL)
            cv2.setWindowProperty('show', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        while True:
            frames, results = self.get_queue()
            if frames is None:
                time.sleep(0.001)
                continue
            
            self.run_once(results, frames)

            if show:
                ppl_images = self.draw_images(frames)
                if ppl_images is None:
                    continue
                m_ppl_images = images_automerge(ppl_images, (1920, 1080))
                cv2.imshow('show' ,m_ppl_images)
                key = cv2.waitKey(1)
                if key == 27:
                    break

            # Calculate the next time to send the next frame
            next_time += self.interval
            delay = next_time - time.perf_counter()
            if delay > 0:
                self.stop_event.wait(delay)

            time.sleep(0.001)
        cv2.destroyAllWindows()

    def get_queue(self):
        """
        Get frames and results from queue
        
        Returns:
            frames: np.ndarray
                frames
            results: list
                results
        """
        if self.test_mode:
            raise NotImplementedError("Subclasses must implement 'get_queue' method")
        
        if not self.queue.empty():
            with self.queue_lock:
                frames, results_list = self.queue.get()
        else:
            return None, None

        results_filter = results_list[..., 4] != -1
        results = [results_list[idx][filt] for idx, filt in enumerate(results_filter)]

        return frames, results

    def run_once(self, results):
        raise NotImplementedError("Subclasses must implement 'run_once' method")
    
    def draw_images(self, frames):
        raise NotImplementedError("Subclasses must implement 'draw_images' method")
        

if __name__ == '__main__':
    import os
    from utilities import load_configs
    from nxva.v11 import Detector
    from dotenv import load_dotenv
    
    task_list, hyper_config, streaming_config, cameras_dict, cameras_configs_dict, all_cameras_ids = load_configs()

    load_dotenv()
    host         = os.getenv('HOST')
    web_port     = os.getenv('WEB_SERVER_PORT')
    control_port = os.getenv('CONTROL_SERVER_PORT')
    api_config   = (host, web_port, control_port)

    # Need super_init_(test_mode = True)
    task_name = 'people_tracking'

    if task_name == 'people_tracking':
        from task.people_tracking import MultiPeopleTask
        task_manager = MultiPeopleTask(streaming_config,
                                       cameras_configs_dict[task_name],
                                       cameras_dict[task_name],
                                       hyper_config[task_name],
                                       api_config
                                       ) 

    # streaming
    stream = MultiStreaming(config='./configs/streaming.yaml',
                            reconnect_interval=30,
                            verbose=True
                            )
    stream.init_cameras()
    stream.run()

    # detector
    detector = Detector('./configs/detection_yolo11s.yaml')
    class_names = detector.class_names
    names_class = {name: class_id for class_id, name in class_names.items()}
    model_class_list = []
    class_names  = [config['class'] for _, config in hyper_config.items() if 'class' in config]
    task_class_names = list(set(name for class_name in class_names for name in class_name))
    for task_class_name in task_class_names:
        class_id = names_class.get(task_class_name)
        if class_id != None:
            model_class_list.append(class_id)
    
    detector.classes = model_class_list

    while True:
        frames, status = stream.get_frames(status=True)
        results = detector(frames)

        task_msg = task_manager.run_once(results, frames)

        ppl_images = task_manager.draw_images(frames)
        m_ppl_images = images_automerge(ppl_images, (1920, 1080))

        cv2.imshow('show' ,m_ppl_images)
        key = cv2.waitKey(1)
        if key == 27:
            break
        time.sleep(0.001)
    cv2.destroyAllWindows()