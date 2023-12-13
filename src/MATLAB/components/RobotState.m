classdef RobotState
    properties(Access = private)
        v;
        w;
    end
    
    methods
        function obj = RobotState(v, w)
            obj.v = v; obj.w = w;
        end
    end
end

