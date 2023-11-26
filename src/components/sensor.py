from components.motion import Pose

class DistanceSensor:
    def __init__(self, environment):
        self._environment = environment
        self._pose = Pose()
        self._value = [0.0]

    def update_pose(self, x, y, theta):
        self._pose.x = x
        self._pose.y = y
        self._pose.theta = theta

    def get_pose(self):
        return self._pose

    def get_environment(self):
        return self._environment

    def sense(self):
        pass

    def get_sensor_reading(self):
        return self._value


class LaserSensor:
    def __init__(self, environment, sensor_offsets):
        self._environment = environment
        self._sensor_offsets = sensor_offsets
        self._pose = Pose()
        self._value = [0.0 for _ in range(len(sensor_offsets))]

    def update_pose(self, x, y, theta):
        self._pose.x = x
        self._pose.y = y
        self._pose.theta = theta

    def get_pose(self):
        return self._pose

    def get_environment(self):
        return self._environment

    def get_sensor_offsets(self):
        return self._sensor_offsets

    def sense(self):
        pass

    def get_sensor_reading(self):
        return self._value
    