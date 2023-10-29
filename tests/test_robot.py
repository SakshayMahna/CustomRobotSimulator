import pytest
from unittest.mock import Mock
from math import pi

import sys
sys.path.append('../src')
from components.robot import Robot, RobotState

class TestRobotState:
    def test_initialize_default_state(self):
        state = RobotState()
        assert state.v == 0
        assert state.w == 0

    def test_initialize_given_state(self):
        state = RobotState(1, 2)
        assert state.v == 1
        assert state.w == 2

class TestRobot:
    @pytest.fixture(autouse=True)
    def _setup_test(self):
        motion_model = Mock()
        motion_model.get_pose.return_value = None
        motion_model.move.return_value = None

        sensor = Mock()
        sensor.sense.return_value = None

        self._robot = Robot(motion_model)
        self._motion_model = motion_model
        self._sensor = sensor

    def test_initialize_robot(self):
        robot = self._robot
        pose = robot.get_pose()
        
        self._motion_model.get_pose.assert_called()

    def test_move_robot(self):
        robot = self._robot
        robot.move(0)
        
        self._motion_model.move.assert_called()

    def test_sense_robot(self):
        robot = self._robot
        robot.add_sensor(self._sensor)
        robot.sense()

        self._sensor.sense.assert_called()


    