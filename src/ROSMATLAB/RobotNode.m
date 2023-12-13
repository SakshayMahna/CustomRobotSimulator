classdef RobotNode < handle
    properties(Constant)
        LINEARSCALE = 120.0;
        ANGULARSCALE = 1.0;
    end

    properties(Access = private)
        robot
        robotNode
        velSubscriber
        scanPublisher
        simTimer
    end
    
    methods
        function obj = RobotNode(robot)
            obj.robot = robot;
            obj.robotNode = ros2node('robot_node');
            obj.initializeSubscribers();
            obj.initializePublishers();
        end
    end

    methods(Access = private)
        function initializeSubscribers(obj)
            obj.velSubscriber = ros2subscriber(obj.robotNode, "/cmd_vel", ...
                           "geometry_msgs/Twist", @obj.velCallback);
        end

        function velCallback(obj, msg)
            velocity = msg.linear.x * obj.LINEARSCALE;
            obj.robot.set_velocity(velocity);

            angular_velocity = msg.angular.z * obj.ANGULARSCALE;
            obj.robot.set_angular_velocity(angular_velocity);
        end

        function initializePublishers(obj)
            obj.scanPublisher = ros2publisher(obj.robotNode, "/scan", ...
                            "sensor_msgs/LaserScan");
            scanCallback(obj);
            obj.simTimer = timer('TimerFcn', @(~, ~) obj.scanCallback(), ...
                                 'ExecutionMode', 'fixedRate', 'Period', 1);
            start(obj.simTimer);
        end

        function scanCallback(obj)
            msg = ros2message("sensor_msgs/LaserScan");
            
            msg.header.stamp = ros2time(obj.robotNode, "now");
            msg.header.frame_id = 'base_laser';

            laserValues = double(obj.robot.get_sensor_reading());
            offsetValues = double(obj.robot.get_sensor_offsets());
            scaledValues = single(laserValues / obj.LINEARSCALE);

            msg.angle_min = single(offsetValues(1));
            msg.angle_max = single(offsetValues(end));
            msg.angle_increment = single((offsetValues(end) - offsetValues(1)) / (length(offsetValues) - 1));
            msg.time_increment = single(0.01);
            msg.scan_time = single(0.5);
            msg.range_min = single(0.0);
            msg.range_max = single(20.0);
            msg.ranges = scaledValues;

            send(obj.scanPublisher, msg);
        end
    end
end

