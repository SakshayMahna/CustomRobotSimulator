import pytest
from numpy import array
from unittest.mock import Mock
from math import pi

import sys
sys.path.append('../src')
from utils.dfs import GridDepthFirstSearch

class TestDepthFirstSearch:
    def test_search1(self):
        grid = array([
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ])

        start_point = [2, 0]
        dfs = GridDepthFirstSearch(grid)
        point = dfs.search(start_point)

        assert point[0] == 0
        assert point[1] == 10

    def test_search2(self):
        grid = array([
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ])

        start_point = [0, 0]
        dfs = GridDepthFirstSearch(grid)
        point = dfs.search(start_point)

        assert point[0] == 3
        assert point[1] == 8