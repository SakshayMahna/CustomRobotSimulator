import rclpy
from ros_node import AlgorithmNode
from random import random

STOP_STATE = 0
MOVE_STATE = 1
ROTATE_STATE = 2

class Wander(AlgorithmNode):
    def __init__(self):
        super().__init__()
        self._counter = 0
        self._rotation_flag = False
        self._state = STOP_STATE 

    def algorithm(self):
        sensor_reading = self.get_sensor_reading()
        scan = abs(sensor_reading[0])

        if self._state == MOVE_STATE:
            if scan < 100:
                self._state = ROTATE_STATE
                self._counter = 0
            else:
                velocity = 1.0
                self.set_velocity(velocity)
                angular_velocity = 0.0
                self.set_angular_velocity(angular_velocity)
        elif self._state == ROTATE_STATE:
            if self._counter == 0:
                velocity = 0.0
                self.set_velocity(velocity)

                angular_velocity = random()
                self.set_angular_velocity(angular_velocity)
            elif self._counter == 500:
                self._state = MOVE_STATE

            self._counter = self._counter + 1
        else:
            self._state = MOVE_STATE


if __name__ == "__main__":
    rclpy.init()
    algorithm = Wander()
    
    algorithm.start()
    rclpy.spin(algorithm)
    
    algorithm.stop()
    algorithm.destroy_node()
    rclpy.shutdown()
