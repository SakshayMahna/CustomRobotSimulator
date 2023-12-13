classdef Pose < handle
    properties
        x;
        y;
        theta;
    end
    
    methods
        function obj = Pose(x, y, theta)
            obj.x = x;
            obj.y = y;
            obj.theta = theta;
        end
    end
end

