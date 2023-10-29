

class DepthFirstSearch:
    def search(self, start_point):
        stack = []
        visited = set()

        self._add_point_to_stack(start_point, stack)

        while stack:
            vertex = self._get_vertex_from_stack(stack)
            
            reached = self._check_reached(vertex)
            if reached:
                self._add_vertex_to_stack(vertex, stack)
                break

            if vertex in visited:
                continue
            visited.add(vertex)

            neighbors = self._get_point_neighbors(vertex)
            for neighbor in neighbors:
                self._add_point_to_stack(neighbor, stack)

        return self._get_point_from_stack(stack)

    def _add_point_to_stack(self, point, stack):
        pass

    def _add_vertex_to_stack(self, vertex, stack):
        pass

    def _get_vertex_from_stack(self, stack):
        pass

    def _get_point_from_stack(self, stack):
        pass
    
    def _check_reached(self, vertex):
        pass

    def _get_point_neighbors(self, vertex):
        pass


class GridDepthFirstSearch(DepthFirstSearch):
    def __init__(self, grid):
        self._grid = grid
        self._rows = len(self._grid)
        self._cols = len(self._grid[0])

    def _transform_point_to_vertex(self, point):
        index = point[0] * self._cols + point[1]
        return index

    def _transform_vertex_to_point(self, vertex):
        rows = len(self._grid)
        cols = len(self._grid[0])
        point = [0, 0]
        point[0] = int(vertex / self._cols)
        point[1] = vertex % self._cols
        return point

    def _add_point_to_stack(self, point, stack):
        vertex = self._transform_point_to_vertex(point)
        stack.append(vertex)

    def _add_vertex_to_stack(self, vertex, stack):
        stack.append(vertex)

    def _get_vertex_from_stack(self, stack):
        vertex = stack.pop()
        return vertex

    def _get_point_from_stack(self, stack):
        vertex = stack.pop()
        point = self._transform_vertex_to_point(vertex)
        return point
    
    def _check_reached(self, vertex):
        reached = False
        point = self._transform_vertex_to_point(vertex)
        if self._grid[point[0]][point[1]] == 0:
            reached = True
        
        return reached

    def _get_point_neighbors(self, vertex):
        point = self._transform_vertex_to_point(vertex)
        neighbors = []

        if point[0] - 1 >= 0:
            n = [point[0] - 1, point[1]]
            neighbors.append(n)
        if point[0] + 1 < self._rows:
            n = [point[0] + 1, point[1]]
            neighbors.append(n)
        if point[1] - 1 >= 0:
            n = [point[0], point[1] - 1]
            neighbors.append(n)
        if point[1] + 1 < self._cols:
            n = [point[0], point[1] + 1]
            neighbors.append(n)
        if point[0] - 1 >= 0:
            if point[1] - 1 >= 0:
                n = [point[0] - 1, point[1] - 1]
                neighbors.append(n)
            if point[1] + 1 < self._cols:
                n = [point[0] - 1, point[1] + 1]
                neighbors.append(n)
        if point[0] + 1 < self._rows:
            if point[1] - 1 >= 0:
                n = [point[0] + 1, point[1] - 1]
                neighbors.append(n)
            if point[1] + 1 < self._cols:
                n = [point[0] + 1, point[1] + 1]
                neighbors.append(n)

        return neighbors