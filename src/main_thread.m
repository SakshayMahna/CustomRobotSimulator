%% Use Python Virtual Environment
pythonPath = "C:\\Personal\\Robot\\Mobile Robots\\" + ...
             "LocalizationExperiment\\CustomRobotSimulator\\" + ...
             "rsim\\Scripts\\python.exe";
pyenv('Version', pythonPath, 'ExecutionMode', 'OutOfProcess');

[robot, sensor] = pyrunfile('main_thread.py', ["robot", "sensor"]);
robotNode = RobotNode(robot);

% p = parpool(2);
% navNode = parfeval(p, @exampleHelperRobotWallFollowingNode, 0);
% slamNode = parfeval(p, @exampleHelperSlamManagerNode, 0);