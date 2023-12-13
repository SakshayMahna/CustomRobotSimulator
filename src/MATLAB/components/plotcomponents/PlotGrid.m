classdef PlotGrid < Grid
    methods
        function collisionObjects = getCollisionObject(obj)
            collisionObjects = cell(1, numel(obj.obstacles));
            for i = 1:numel(obj.obstacles)
                collisionObjects{i} = obj.obstacles{i}.getCollisionObject();
            end
        end
    end
end