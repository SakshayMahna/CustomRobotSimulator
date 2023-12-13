% Obstacle Aggregate
classdef Grid < handle
    properties(Access = private)
        obstacles;
        position;
    end
    
    methods
        function obj = Grid()
            obj.obstacles = [];
            obj.position = 0;
        end
        
        function obstacle = getNextObstacle(obj)
            if obj.position < length(obj.obstacles)
                obstacle = obj.obstacles{obj.position};
                obj.position = obj.position + 1;
            else
                obstacle = [];
                obj.resetPosition();
            end
        end
        
        function addObstacle(obj, obstacle)
            obj.obstacles = [obj.obstacles, {obstacle}];
        end
    end

    methods(Access = private)
        function resetPosition(obj)
            obj.position = 0;
        end
    end
end

