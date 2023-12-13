classdef LaserSensor
    properties(Access = private)
        environment
        sensorOffsets
        pose
        value
    end
    
    methods
        function obj = LaserSensor(environment, sensorOffsets)
            obj.environment = environment;
            obj.sensorOffsets = sensorOffsets;
            obj.pose = Pose(0, 0, 0);
            obj.value = zeros(1, length(sensor_offsets));
        end
        
        function updatePose(obj, x, y, theta)
            obj.pose.x = x;
            obj.pose.y = y;
            obj.pose.theta = theta;
        end
        
        function pose = getPose(obj)
            pose = obj.pose;
        end
        
        function environment = getEnvironment(obj)
            environment = obj.environment;
        end
        
        function sensorOffsets = getSensorOffsets(obj)
            sensorOffsets = obj.sensorOffsets;
        end
        
        function sense(obj)
            % Implement sensing logic here
            % For Child Class
        end
        
        function sensorReading = getSensorReading(obj)
            sensorReading = obj.value;
        end
    end
end

