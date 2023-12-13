import pygame
import random
from math import pi
from components.motion import Pose, UnicycleModel
from physics_engine.physics_engine import PygamePhysicsEngine
from physics_engine.actors import (PERobotActor, PEGridActor, 
                                   PEDistanceSensorActor, PELaserSensorActor)
from visual_engine.visual_engine import PygameVisualEngine
from visual_engine.actors import (VERobotActor, VEGridActor, 
                                  VEDistanceSensorActor, VELaserSensorActor)
from components.pygame_components import (PygameRobot, 
                                          PygameDistanceSensor, PygameLaserSensor, 
                                          PygameRectangleObstacle, PygameGrid)

from threading import Thread

def create_grid():
    grid = PygameGrid()

    obstacle = PygameRectangleObstacle(440, 160, 300, 300)
    grid.add_obstacle(obstacle)

    return grid

def create_robot():
    motion_model = UnicycleModel(Pose(340, 60, -pi/6))
    robot = PygameRobot(motion_model)

    return robot

def create_sensor(grid):
    sensor = PygameDistanceSensor(grid)
    return sensor

def create_laser_sensor(grid):
    resolution = 0.005
    start_angle = -0.3; end_angle = 0.3
    angle_range = end_angle - start_angle
    angle_length = int(angle_range / resolution)
    sensor_offsets = [start_angle + i * resolution for i in range(angle_length + 1)]
    sensor = PygameLaserSensor(grid, sensor_offsets)
    return sensor

def execute(ve, pe):
    running = ve.initialize()
    while running:
        running = ve.render()
        pe.step()

    ve.terminate()

if __name__ == "__main__":
    ve = PygameVisualEngine()
    pe = PygamePhysicsEngine(0.01)

    grid = create_grid()
    ve.add_actor(VEGridActor(grid))
    pe.add_actor(PEGridActor(grid))

    robot = create_robot()
    ve.add_actor(VERobotActor(robot))
    pe.add_actor(PERobotActor(robot))

    sensor = create_laser_sensor(grid)
    robot.add_sensor(sensor)
    ve.add_actor(VELaserSensorActor(sensor))
    pe.add_actor(PELaserSensorActor(sensor))
    
    Thread(target = execute, args=(ve, pe)).start()