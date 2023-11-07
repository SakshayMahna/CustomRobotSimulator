import pytest
from math import pi

import sys
sys.path.append('../src')
from components.motion import Pose, UnicycleModel

class TestPose:
    def test_initialize_default_pose(self):
        pose = Pose()
        assert pose.x == 0
        assert pose.y == 0
        assert pose.theta == 0

    def test_initialize_given_pose(self):
        pose = Pose(1, 2, 3)
        assert pose.x == 1
        assert pose.y == 2
        assert pose.theta == 3

class TestUnicycleModel:
    @pytest.fixture(autouse=True)
    def _setup_test(self):
        init_pose = Pose()
        self._model = UnicycleModel(init_pose)

    def test_move_straight_line(self):
        model = self._model

        # Heading angle = 0
        v = 1; w = 0; dt = 1
        poses_theta0 = [
            [0, 0, 0], [1, 0, 0], [2, 0, 0], [3, 0, 0], [4, 0, 0], 
            [5, 0, 0], [6, 0, 0], [7, 0, 0], [8, 0, 0], [9, 0, 0], [10, 0, 0]
        ]

        for t in range(1, 11, dt):
            model.move(v, w, dt)
            pose = model.get_pose()
            pose_array = [pose.x, pose.y, pose.theta]
            assert pose_array == poses_theta0[t]
            
        # Heading angle = pi/3
        heading_angle = pi/3;
        init_pose = Pose(0, 0, heading_angle)
        model = UnicycleModel(init_pose)
        
        v = 1; w = 0; dt = 1
        poses_theta30 = [
            [0, 0, heading_angle], [0.5, 0.866, heading_angle], [1, 1.732, heading_angle]
        ];
        
        for t in range(1, 3, dt):
            model.move(v, w, dt)
            pose = model.get_pose()
            assert pose.x == pytest.approx(poses_theta30[t][0], 0.001)
            assert pose.y == pytest.approx(poses_theta30[t][1], 0.001)
            assert pose.theta == pytest.approx(poses_theta30[t][2], 0.001)

    def test_rotate(self):
        model = self._model
        
        v = 0; w = (2 * pi) / 4; dt = 1;
        poses_rotate = [
            [0, 0, 0], [0, 0, pi/2],
            [0, 0, pi], [0, 0, 3*pi/2],
            [0, 0, 0], [0, 0, pi/2]
        ]
        for t in range(1, 6, dt):
            model.move(v, w, dt)
            pose = model.get_pose()
            assert pose.x == pytest.approx(poses_rotate[t][0], 0.001)
            assert pose.y == pytest.approx(poses_rotate[t][1], 0.001)
            assert pose.theta == pytest.approx(poses_rotate[t][2], 0.001)