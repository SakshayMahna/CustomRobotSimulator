import pygame
from math import degrees
from visual_engine.utils import determine_line_box_clip

class VEActor:
    def __init__(self, component):
        self._component = component

    def draw(self, screen):
        pass

class VERobotActor(VEActor):
    def draw(self, screen):
        robot = self._component
        pose = robot.get_pose()
        draw_points = robot.get_visual_object()

        rotated_points = [p.rotate(degrees(pose.theta)) for p in draw_points]
        triangle_points = [(pygame.Vector2(pose.x, pose.y) + p*1) for p in rotated_points]
        pygame.draw.polygon(screen, "blue", triangle_points)

class VEDistanceSensorActor(VEActor):
    def draw(self, screen):
        sensor = self._component
        grid = sensor.get_environment()
        pose = sensor.get_pose()
        [width, height] = screen.get_size()

        start_pos = pygame.Vector2(pose.x, pose.y)

        (ex, ey) = determine_line_box_clip(pose.x, pose.y, pose.theta, width, height)
        end_pos = pygame.Vector2(ex, ey)
        end_pos = self._determine_clip_point(grid, start_pos, end_pos)

        pygame.draw.circle(screen, "red", end_pos, 5)
        pygame.draw.line(screen, "red", start_pos, end_pos)

        sensor.update_visual_object(start_pos.x, start_pos.y, end_pos.x, end_pos.y)

    def _determine_clip_point(self, grid, start_pos, end_pos):
        for obstacle_component in grid:
            obstacle = obstacle_component.get_collision_object()
            contact_points = obstacle.clipline(start_pos, end_pos)
            if contact_points:
                contact_point = contact_points[0]
                end_pos = pygame.Vector2(contact_point[0], contact_point[1])
                break

        return end_pos

        
class VEGridActor(VEActor):
    def draw(self, screen):
        grid = self._component
        for obstacle in grid:
            visual_object = obstacle.get_visual_object()
            pygame.draw.rect(screen, "black", visual_object)

