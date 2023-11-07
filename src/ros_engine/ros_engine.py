import rclpy
from rclpy.executors import MultiThreadedExecutor
from threading import Thread

class ROSEngine:
    def __init__(self):
        rclpy.init()
        self._executor = MultiThreadedExecutor()
        self._main_thread = Thread(target = self._executor.spin)

    def add_node(self, node):
        self._executor.add_node(node)

    def start_engine(self):
        self._main_thread.start()

    def stop_engine(self):
        rclpy.shutdown()
        self._main_thread.join()