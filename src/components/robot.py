from math import pi, sin, cos

class RobotState:
    def __init__(self, v = 0, w = 0):
        self.v = v
        self.w = w

class Robot:
    def __init__(self, motion_model):
        self._motion_model = motion_model
        self._sensor = None
        self._robot_state = RobotState()

    def get_pose(self):
        pose = self._motion_model.get_pose()
        return pose

    def set_velocity(self, v):
        self._robot_state.v = v

    def set_angular_velocity(self, w):
        self._robot_state.w = w

    def add_sensor(self, sensor):
        self._sensor = sensor

    def move(self, dt):
        v = self._robot_state.v
        w = self._robot_state.w
        self._motion_model.move(v, w, dt)
        self._update_sensor_pose()

    def _update_sensor_pose(self):
        if self._sensor:
            pose = self.get_pose()
            self._sensor.update_pose(pose.x, pose.y, pose.theta)

    def get_sensor_reading(self):
        sensor = self._sensor
        return sensor.get_sensor_reading()

    def accept(self, visitor):
        visitor.visit(self)

    