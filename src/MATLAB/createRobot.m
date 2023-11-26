function robot = createRobot(environment)
    huskyRobot = loadrobot("clearpathHusky");
    robot = robotPlatform("husky", environment, RigidBodyTree=huskyRobot, ...
                          InitialBasePosition=[1 1 0.12]);
end

