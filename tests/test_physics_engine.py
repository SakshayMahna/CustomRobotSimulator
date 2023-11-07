import pytest
from numpy import unique

import sys
sys.path.append('../src')
from grid import Grid

class TestGrid:
    def test_initialize_empty_grid_default_dimensions(self):
        grid = Grid()
        grid_array = grid.get_array()
        rows = len(grid_array); cols = len(grid_array[0])
        
        assert rows == 600
        assert cols == 600

    def test_initialize_empty_grid_given_dimensions(self):
        grid = Grid(500, 500)
        grid_array = grid.get_array()
        rows = len(grid_array); cols = len(grid_array[0])
        
        assert rows == 500
        assert cols == 500

    def test_initialize_grid_given_map(self):
        grid = Grid()
        grid.load_map("map.png")
        grid_array = grid.get_array()

        grid_unique = unique(grid_array)
        assert len(grid_unique) == 2
        assert grid_unique[0] == 0
        assert grid_unique[1] == 255
        