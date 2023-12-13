classdef PlotRectangleObstacle < RectangleObstacle
    properties
        visualObject
        collisionObject
    end
    
    methods
        function obj = PlotRectangleObstacle(left, top, width, height)
            obj = obj@RectangleObstacle(left, top, width, height);
            obj.initializeVisualObject();
            obj.initializeCollisionObject();
        end
        
        function initializeVisualObject(obj)
            [l, t, w, h] = obj.getDimensionsLTWH();
            obj.visualObject = polyshape([l, l + w, l + w, l], ...
                                          [t, t, t - h, t - h]);
        end
        
        function initializeCollisionObject(obj)
            obj.collisionObject = obj.visualObject;
        end
        
        function collisionObject = getCollisionObject(obj)
            collisionObject = obj.collisionObject;
        end
        
        function visualObject = getVisualObject(obj)
            visualObject = obj.visualObject;
        end
    end
end