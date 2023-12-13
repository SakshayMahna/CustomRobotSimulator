classdef TFNode < handle
    properties(Constant)
        LINEARSCALE = 150.0;
        ANGULARSCALE = 1.0;
    end

    properties(Access = private)
        robot
        sensor
        tfNode
        tftree
    end
    
    methods
        function obj = TFNode(robot, sensor)
            obj.robot = robot;
            obj.sensor = sensor;
            obj.tfNode = ros2node('static_tf_node');

            obj.initializeTFTree();
            obj.createTransform();
        end
    end
    methods(Access = private)
        function initializeTFTree(obj)
            obj.tftree = ros2tf(obj.tfNode, 'StaticBroadcasterQoS', ...
                         struct('Depth', 50));
        end

        function createTransform(obj)
            robotPose = obj.robot.get_pose();
            sensorPose = obj.sensor.get_pose();

            dx = (sensorPose.x - robotPose.x) / obj.LINEARSCALE;
            dy = (sensorPose.y - robotPose.y) / obj.LINEARSCALE;
            dtheta = (sensorPose.theta - robotPose.theta) / obj.ANGULARSCALE;

            translation = double([dx, dy, 0.0]);
            rotation = double(eul2quat([dtheta, 0.0, 0.0]));
            header = ros2time(obj.tfNode, 'now');

            tfmsg1 = obj.newTransformStamped(header, 'base_link', 'base_laser', ...
                                             translation, rotation);

            translation = double([0.0, 0.0, 0.0]);
            rotation = double(eul2quat([0.0, 0.0, 0.0]));
            tfmsg2 = obj.newTransformStamped(header, 'base_footprint', 'base_link', ...
                                             translation, rotation);

            sendTransform(obj.tftree, tfmsg1);
            sendTransform(obj.tftree, tfmsg2);
        end

        function tfStampedMsg = newTransformStamped(~, header, targetFrame, ...
                                sourceFrame, translation, rotation)
            tfStampedMsg = ros2message('geometry_msgs/TransformStamped');
            tfStampedMsg.child_frame_id = sourceFrame;
            tfStampedMsg.header.frame_id = targetFrame;
            tfStampedMsg.header.stamp = header;
            
            tfStampedMsg.transform.translation.x = translation(1);
            tfStampedMsg.transform.translation.y = translation(2);
            tfStampedMsg.transform.translation.z = translation(3);
            
            tfStampedMsg.transform.rotation.w = rotation(1);
            tfStampedMsg.transform.rotation.x = rotation(2);
            tfStampedMsg.transform.rotation.y = rotation(3);
            tfStampedMsg.transform.rotation.z = rotation(4);
        end
    end
end

