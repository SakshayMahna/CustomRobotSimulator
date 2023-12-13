classdef RectangleObstacle < handle
    properties(Access = private)
        left;
        top;
        width;
        height;
    end
    
    methods
        function obj = RectangleObstacle(l, t, w, h)
            obj.left = l; obj.top = t;
            obj.width = w; obj.height = h;
        end
        
        function dim = getDimensionsLTWH(obj)
            dim = [obj.left, obj.top, obj.width, obj.height];
        end
    end
end

