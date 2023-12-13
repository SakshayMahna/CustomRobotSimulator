function exampleHelperRobotWallFollowingNode
    %% Parameters
    pivotRegionWidth = 0.266; % Width of region in front of robot to check for head-on wall
    pivotDist = 0.65; % Length of region ahead of robot to check for head-on wall (centered on LiDAR)
    pivotSpeed = 0.6; % Rate at which robot will turn in place when it sees a head-on wall
    wallProbeAngle = -0.2; % Center angle of wall-following probe region
    wallProbeWidth = 5*pi/180; % Angle spread of wall-following probe region
    linearSpeed = 0.2; % Robot's base forward speed
    deadzone = 0.05; % Region around target distance where robot will simply go straight
    steerMult = 2.5; % Factor mapping probe distance to steering input
    triggerDist = 0.65; % Target distance for wall-following probe
    maxDist = 0.2; % Any deviation from the target distance greater than this will be trated at a deviation of max_dist

    %% Initialization
    node = ros2node("wall_follow_node");
    lidarSubscriber = ros2subscriber(node, '/scan', 'sensor_msgs/LaserScan');
    cmdPublisher = ros2publisher(node, '/cmd_vel', 'geometry_msgs/Twist');
    startNavSubscriber = ros2subscriber(node, '/start_navigation', 'std_msgs/Empty', @startNavigationCallback);
    stopNavSubscriber = ros2subscriber(node, '/stop_navigation', 'std_msgs/Empty', @stopNavigationCallback);
    closeNodeSubscriber = ros2subscriber(node, '/close_navigation', 'std_msgs/Empty', @closeNodeCallback);
    rate = ros2rate(node, 10);
    
    %% State Flags
    navigateFlag = true; % Decide whether the robot should be idle or navigating
    runningFlag = true; % Whether to keep the node running

    %% Control Loop
    while runningFlag
        if navigateFlag
            lidarMsg = lidarSubscriber.LatestMessage;
            if ~isempty(lidarMsg) && ~isempty(cmdPublisher)
                cmdMsg = navStep(lidarMsg);
                send(cmdPublisher, cmdMsg);
            end
        else
            cmdMsg = ros2message(cmdPublisher);
            cmdMsg.linear.x = 0;
            cmdMsg.angular.z = 0;
            send(cmdPublisher, cmdMsg);
        end
        waitfor(rate);
    end

    cmdMsg = ros2message(cmdPublisher);
    cmdMsg.linear.x = 0;
    cmdMsg.angular.z = 0;
    send(cmdPublisher, cmdMsg);

    %% Helper Functions
    function cmdMsg = navStep(lidarMsg)
        t0 = lidarMsg.angle_min;
        t1 = lidarMsg.angle_max;
        dt = lidarMsg.angle_increment;
        R = lidarMsg.ranges;
        %R(isinf(R)) = NaN;
        theta = (t0:dt:t1)';

        xs = R.*cos(theta);
        ys = R.*sin(theta);

        inds = (theta >= wallProbeAngle - wallProbeWidth/2) & (theta <= wallProbeAngle + wallProbeWidth/2);
        medianRange = median(R(inds));
        currentDistance = medianRange - triggerDist;

        cmdMsg = ros2message('geometry_msgs/Twist');
        if any((abs(ys) <= pivotRegionWidth/2) & (xs > 0) & (xs <= pivotDist)) % Pivot
            cmdMsg.linear.x = 0;
            cmdMsg.angular.z = pivotSpeed;
        elseif abs(currentDistance) < deadzone/2 % Straight
            cmdMsg.linear.x = linearSpeed;
            cmdMsg.angular.z = 0;
        else % Turning
            dist = maxDist;
            if ~isinf(currentDistance)
                dist = double(sign(currentDistance)*min([abs(currentDistance), maxDist])); % Coder complains about type mismatch without double()
            end
            cmdMsg.linear.x = double(linearSpeed); % Coder complains about type mismatch without double()
            cmdMsg.angular.z = double(-steerMult*dist); % Coder complains about type mismatch without double()
        end
    end

    %% Callbacks
    function startNavigationCallback(~, ~)
        navigateFlag = true;
    end
    function stopNavigationCallback(~, ~)
        navigateFlag = false;
    end
    function closeNodeCallback(~, ~)
        runningFlag = false;
    end
end