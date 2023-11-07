import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from datetime import datetime
from threading import Thread
import time

class AlgorithmNode(Node):
    def __init__(self):
        super().__init__('algorithm_node')
        self._initialize_variables()
        self._initialize_subscribers()
        self._initialize_publishers()

        self._time_cycle = 60
        self._main_thread = Thread(target = self._run_algorithm)

    def _initialize_variables(self):
        self._velocity = 0.0
        self._angular_velocity = 0.0
        self._sensor_reading = [0.0]

    def _initialize_subscribers(self):
        self._scan_subscriber = self.create_subscription(LaserScan, 'scan',
                                self._scan_callback, 10)

    def _initialize_publishers(self):
        self._vel_publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        timer_period = 0.5
        self.create_timer(timer_period, self._vel_callback)

    def _run_algorithm(self):
        time_cycle = self._time_cycle
        while True:
            start_time = datetime.now()
            self.algorithm()
            end_time = datetime.now()

            dt = end_time - start_time
            ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
            if(ms < time_cycle):
                time.sleep((time_cycle - ms) / 1000.0)

    def _scan_callback(self, msg):
        self._sensor_reading = msg.ranges

    def _vel_callback(self):
        msg = Twist()
        msg.linear.x = self._velocity
        msg.angular.z = self._angular_velocity
        self._vel_publisher.publish(msg)

    def set_velocity(self, v):
        self._velocity = v

    def set_angular_velocity(self, w):
        self._angular_velocity = w

    def get_sensor_reading(self):
        return self._sensor_reading

    def start(self):
        self._main_thread.start()

    def stop(self):
        self._main_thread.join()

    def algorithm(self):
        pass