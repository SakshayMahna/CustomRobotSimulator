classdef PlotRobot < Robot
    properties(Access = private)
        drawPoints;
        side;
        collisionObject;
    end
    
    methods
        function obj = PlotRobot(motionModel)
            obj = obj@Robot(motionModel);
            obj.initializeVisualObject();
            obj.initializeCollisionObject();
        end
        
        function initializeVisualObject(obj)
            obj.drawPoints = [
                [-5, -8.66]; 
                [-5, 8.66]; 
                [20.0, 0.0]
            ];
        end
        
        function initializeCollisionObject(obj)
            side = 30;
            pose = obj.getPose();
            obj.side = side;
            obj.collisionObject = polyshape([pose.x - side/2, pose.x + side/2, pose.x + side/2, pose.x - side/2], ...
                                            [pose.y + side/2, pose.y + side/2, pose.y - side/2, pose.y - side/2]);
        end
        
        function collisionObject = getCollisionObject(obj)
            collisionObject = obj.collisionObject;
        end
        
        function updateCollisionObject(obj)
            side = obj.side;
            pose = obj.getPose();
            obj.collision_object = polyshape([pose.x - side/2, pose.x + side/2, pose.x + side/2, pose.x - side/2], ...
                                            [pose.y + side/2, pose.y + side/2, pose.y - side/2, pose.y - side/2]);
        end
        
        function visualObject = getVisualObject(obj)
            visualObject = obj.draw_points;
        end
    end
end