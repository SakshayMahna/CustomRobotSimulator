import pygame
import random
from math import pi
from components.motion import Pose, UnicycleModel
from physics_engine.physics_engine import PygamePhysicsEngine
from physics_engine.actors import PERobotActor, PEGridActor, PEDistanceSensorActor
from visual_engine.visual_engine import PygameVisualEngine
from visual_engine.actors import VERobotActor, VEGridActor, VEDistanceSensorActor
from components.pygame_components import (PygameRobot, PygameDistanceSensor, 
                                          PygameRectangleObstacle, PygameGrid)

def create_grid():
    grid = PygameGrid()

    obstacle = PygameRectangleObstacle(1000, 200, 300, 400)
    grid.add_obstacle(obstacle)

    obstacle = PygameRectangleObstacle(0, 270, 500, 100)
    grid.add_obstacle(obstacle)

    return grid

def create_robot():
    motion_model = UnicycleModel(Pose(540, 360, -pi/6))
    robot = PygameRobot(motion_model)

    return robot

def create_sensor(grid):
    sensor = PygameDistanceSensor(grid)
    return sensor

if __name__ == "__main__":
    ve = PygameVisualEngine()
    pe = PygamePhysicsEngine(0.01)

    grid = create_grid()
    ve.add_actor(VEGridActor(grid))
    pe.add_actor(PEGridActor(grid))

    robot = create_robot()
    ve.add_actor(VERobotActor(robot))
    pe.add_actor(PERobotActor(robot))

    sensor = create_sensor(grid)
    robot.add_sensor(sensor)
    ve.add_actor(VEDistanceSensorActor(sensor))
    pe.add_actor(PEDistanceSensorActor(sensor))

    running = ve.initialize()

    while running:
        running = ve.render()
        pe.step()

        robot.set_angular_velocity(5)

    ve.terminate()