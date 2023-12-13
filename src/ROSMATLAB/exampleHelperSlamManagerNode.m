function exampleHelperSlamManagerNode
    %% Parameters
    robotLeaveDistance = 2; % Distance robot must travel from start before we start checking that it's returned
    robotReturnDistance = 0.5; % Distance from the start robot must be to finish a lap

    %% Variable Setup
    node = ros2node('slam_node');
    startRobotPublisher = ros2publisher(node, '/start_navigation', 'std_msgs/Empty'); % Publisher to start the robot
    stopRobotPublisher = ros2publisher(node, '/stop_navigation', 'std_msgs/Empty'); % Publisher to stop the robot
    lidarSubscriber = ros2subscriber(node, '/scan', 'sensor_msgs/LaserScan'); % Subscriber to pull lidar scans from the robot

    slamObj = lidarSLAM(20, 8, 1000); % Object that will perform SLAM (map resolution 20, 8m max lidar range, max of 1000 scans)
    slamObj.LoopClosureThreshold = 300; % Raise threshold to prevent smearing

    %% Main Loop
    rate = ros2rate(node, 10);
    robotLeftFlag = false; % Track if the robot has left the start area
    while true
        [lidarMsg,status,~] = receive(lidarSubscriber); % Get the current lidar scan from the robot
    
        if status % If the scan is good, do SLAM
            angles = double(lidarMsg.angle_min:lidarMsg.angle_increment:lidarMsg.angle_max);
            ranges = double(lidarMsg.ranges);
            scan = lidarScan(ranges,angles);                                                      % Build the scan object
            removeInvalidData(scan,RangeLimits=[1/slamObj.MapResolution slamObj.MaxLidarRange]);  % Remove invalid data to avoid errors
            addScan(slamObj,scan);                                                                % Add the scan
            show(slamObj);
        end
    
        send(startRobotPublisher,ros2message(startRobotPublisher)) % Tell the navigation node to move the robot
        waitfor(rate);
    end
end