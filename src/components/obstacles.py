class RectangleObstacle:
    def __init__(self, left = 0, top = 0, width = 100, height = 100):
        self._left = left; self._top = top
        self._width = width; self._height = height

    def get_dimensions_ltwh(self):
        dim = (self._left, self._top, self._width, self._height)
        return dim

# Obstacle Aggregate
class Grid:
    def __init__(self):
        self._obstacles = []
        self._position = 0

    def __iter__(self):
        self._position = 0
        return self

    def __next__(self):
        try:
            obstacle = self._obstacles[self._position]
            self._position += 1
        except:
            raise StopIteration()

        return obstacle

    def add_obstacle(self, obstacle):
        self._obstacles.append(obstacle)

    