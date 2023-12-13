classdef Robot
    properties(Access = private)
        motionModel
        sensor
        robotState
    end
    
    methods
        function obj = Robot(motionModel)
            obj.motionModel = motionModel;
            obj.sensor = [];
            obj.robotState = RobotState(0, 0);
        end
        
        function pose = getPose(obj)
            pose = obj.motionModel.getPose();
        end
        
        function v = getVelocity(obj)
            v = obj.robotState.v;
        end
        
        function w = getAngularVelocity(obj)
            w = obj.robotState.w;
        end
        
        function setVelocity(obj, v)
            obj.robotState.v = v;
        end
        
        function setAngularVelocity(obj, w)
            obj.robotState.w = w;
        end
        
        function addSensor(obj, sensor)
            obj.sensor = sensor;
            obj.updateSensorPose();
        end
        
        function move(obj, dt)
            v = obj.robotState.v;
            w = obj.robotState.w;
            obj.motionModel.move(v, w, dt);
            obj.updateSensorPose();
        end
        
        function updateSensorPose(obj)
            if ~isempty(obj.sensor)
                pose = obj.getPose();
                obj.sensor.updatePose(pose.x, pose.y, pose.theta);
            end
        end
        
        function sensorReading = getSensorReading(obj)
            sensorReading = obj.sensor.getSensorReading();
        end
        
        function sensorOffsets = getSensorOffsets(obj)
            sensorOffsets = obj.sensor.getSensorOffsets();
        end
    end
end
