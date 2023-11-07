from PIL import Image
from numpy import array, unique

class Grid:
    def __init__(self, rows = 600, cols = 600):
        self._grid = array(
            [[1 for j in range(cols)] for i in range(rows)])

    def get_array(self):
        return self._grid

    def load_map(self, src):
        img = Image.open(src)
        rows = len(self._grid); cols = len(self._grid[0])
        img.resize((rows, cols))
        self._grid = array(img)