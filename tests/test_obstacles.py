import pytest
from unittest.mock import Mock
from math import pi

import sys
sys.path.append('../src')
from components.obstacles import RectangleObstacle, Grid

class TestRectangleObstacle:
    def test_initialize_default_obstacle(self):
        obs = RectangleObstacle()
        [l,t,w,h] = obs.get_dimensions_ltwh()
        
        assert l == 0
        assert t == 0
        assert w == 100
        assert h == 100

    def test_initialize_given_obstacle(self):
        obs = RectangleObstacle(1, 2, 3, 4)
        [l,t,w,h] = obs.get_dimensions_ltwh()
        
        assert l == 1
        assert t == 2
        assert w == 3
        assert h == 4

class TestGrid:
    @pytest.fixture(autouse=True)
    def _setup_test(self):
        self._grid = Grid()

    def test_add_obstacles(self):
        grid = self._grid
        obstacle1 = Mock()
        obstacle2 = Mock()

        grid.add_obstacle(obstacle1)
        grid.add_obstacle(obstacle2)

        assert len(list(grid)) == 2

    def test_iterate_obstacles(self):
        grid = self._grid
        obstacle1 = Mock()
        obstacle2 = Mock()

        grid.add_obstacle(obstacle1)
        grid.add_obstacle(obstacle2)

        count = 0
        for obs in grid:
            if count == 0:
                assert obs == obstacle1
            else:
                assert obs == obstacle2
            count = count + 1

        assert count == 2