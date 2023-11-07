import pygame
from math import sqrt
from components.robot import Robot
from components.sensor import DistanceSensor
from components.obstacles import RectangleObstacle, Grid

class PygameRobot(Robot):
    def __init__(self, motion_model):
        super(PygameRobot, self).__init__(motion_model)
        self._initialize_visual_object()
        self._initialize_collision_object()
   
    def _initialize_visual_object(self):
        self._draw_points = [
            pygame.Vector2(-5, -8.66), 
            pygame.Vector2(-5, 8.66), 
            pygame.Vector2(20.0, 0.0)
        ]

    def _initialize_collision_object(self):
        side = 30
        pose = self.get_pose()
        
        self._side = side
        self._collision_object = pygame.Rect(pose.x - side/2, pose.y - side/2, side, side)

    def get_collision_object(self):
        return self._collision_object

    def update_collision_object(self):
        side = self._side
        pose = self.get_pose()
        self._collision_object.update(pose.x - side/2, pose.y - side/2, side, side)

    def get_visual_object(self):
        return self._draw_points

    def accept(self, visitor):
        visitor.visit(self)


class PygameDistanceSensor(DistanceSensor):
    def __init__(self, grid):
        super(PygameDistanceSensor, self).__init__(grid)
        self._initialize_visual_object()
        self._initialize_collision_object()
    
    def _initialize_visual_object(self):
        pose = self.get_pose()
        self._start_pos = pygame.Vector2(pose.x, pose.y)
        self._end_pos = pygame.Vector2(pose.x, pose.y)

    def _initialize_collision_object(self):
        pass

    def sense(self):
        start_pos = self._start_pos
        end_pos = self._end_pos
                
        distance = self._calculate_distance_between_pos(start_pos, end_pos)
        self._value = [distance]

    def _calculate_distance_between_pos(self, pos1, pos2):
        x0 = pos1.x; y0 = pos1.y
        x1 = pos2.x; y1 = pos2.y
        return sqrt((x0-x1)**2 + (y0-y1)**2)

    def get_collision_object(self):
        return (self._start_pos, self._end_pos)

    def get_visual_object(self):
        return (self._start_pos, self._end_pos)

    def update_visual_object(self, sx, sy, ex, ey):
        self._start_pos = pygame.Vector2(sx, sy)
        self._end_pos = pygame.Vector2(ex, ey)


class PygameRectangleObstacle(RectangleObstacle):
    def __init__(self, left, top, width, height):
        super(PygameRectangleObstacle, self).__init__(left, top, width, height)
        self._initialize_visual_object()
        self._initialize_collision_object()
   
    def _initialize_visual_object(self):
        [l,t,w,h] = self.get_dimensions_ltwh()
        self._visual_object = pygame.Rect(l, t, w, h)
    
    def _initialize_collision_object(self):
        self._collision_object = self._visual_object

    def get_collision_object(self):
        return self._collision_object

    def get_visual_object(self):
        return self._visual_object

    def accept(self, visitor):
        visitor.visit(self)

class PygameGrid(Grid):
    def get_collision_object(self):
        for obstacle in self._obstacles:
            yield obstacle.get_collision_object()