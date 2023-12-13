classdef PEActor < handle
    properties(Access = private)
        component
    end
    
    methods
        function obj = PEActor(component)
            obj.component = component;
        end
        
        function step(obj)
            % Implement step logic here
        end
        
        function resolveCollision(obj, dt)
            % Implement collision resolution logic here
        end
        
        function collisionObject = getCollisionObject(obj)
            collisionObject = obj.component.getCollisionObject();
        end
    end
end