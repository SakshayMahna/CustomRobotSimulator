import pytest
from numpy import array
from unittest.mock import Mock
from math import pi

import sys
sys.path.append('../src')
from components.sensor import DistanceSensor
from components.motion import Pose

class TestDistanceSensor:
    def test_initialize_sensor(self):
        environment = Mock()
        sensor = DistanceSensor(environment)

        assert sensor.get_environment() == environment

    def test_sensor_pose(self):
        environment = Mock()
        sensor = DistanceSensor(environment)
        pose = sensor.get_pose()

        assert pose.x == 0
        assert pose.y == 0
        assert pose.theta == 0

        sensor.update_pose(1, 2, 3)

        assert pose.x == 1
        assert pose.y == 2
        assert pose.theta == 3
