%% Initialize Node
robotNode = ros2node('robot_node');

%% Initialize Input for Callbacks
callbackInputs.robot = robot;
callbackInputs.robotNode = robotNode;
callbackInputs.linearScale = 150.0;
callbackInputs.angularScale = 1.0;

%% Initialize Subscriber
velSubscriber = ros2subscriber(robotNode, "/cmd_vel", ...
                "geometry_msgs/Twist", {@velCallback, callbackInputs});

%% Initialize Publisher
scanPublisher = ros2publisher(robotNode, "/scan", ...
                "sensor_msgs/LaserScan");
callbackInputs.scanPublisher = scanPublisher;
callbackInputs.scanMessage = createScanMessage();
simTimer = ExampleHelperROSTimer(0.1, {@scanCallback, callbackInputs});

%% Callbacks
function velCallback(msg, handle)
    velocity = msg.linear.x * handle.linearScale;
    handle.robot.set_velocity(velocity);

    angular_velocity = msg.angular.z * handle.angularScale;
    handle.robot.set_angular_velocity(angular_velocity);
end

function createScanMessage()

function scanCallback(~, ~, handle)
    msg = ros2message("sensor_msgs/LaserScan");
    
    msg.header.stamp = ros2time(handle.robotNode, "now");
    msg.header.frame_id = 'base_laser';

    laserValues = handle.robot.get_sensor_reading();
    offsetValues = handle.robot.get_sensor_offsets();
    scaledValues = laserValues / handle.linearScale;

    msg.angle_min = offsetValues(1);
    msg.angle_max = offsetValues(end);
    msg.angle_increment = (offsetValues(end) - offsetValues(1)) / (length(offsetValues) - 1);
    msg.time_increment = 0.01;
    msg.scan_time = 0.5;
    msg.range_min = 0.0;
    msg.range_max = 20.0;
    msg.ranges = scaledValues;

    send(handle.scanPublisher, msg);
end