classdef PERobotActor < PEActor
    methods
        function obj = PERobotActor(component)
            obj = obj@PEActor(component);
        end
        
        function step(obj, dt)
            obj.updatePose(dt);
        end
        
        function resolveCollision(obj, dt)
            obj.updatePose(-dt);
        end
    end
    
    methods (Access = private)
        function updatePose(obj, dt)
            robot = obj.component;
            robot.move(dt);
            robot.updateCollisionObject();
        end
    end
end