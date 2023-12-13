classdef PlotLaserSensor < LaserSensor
    properties (Access = private)
        startPos
        endPoses
    end
    
    methods
        function obj = PlotLaserSensor(grid, sensorOffsets)
            obj = obj@LaserSensor(grid, sensorOffsets);
            obj.initializeVisualObject();
            obj.initializeCollisionObject();
        end
        
        function initializeVisualObject(obj)
            pose = obj.getPose();
            sensorOffsets = obj.getSensorOffsets();
            obj.startPos = [pose.x, pose.y];
            obj.endPoses = repmat([pose.x, pose.y], length(sensorOffsets), 1);
        end
        
        function initializeCollisionObject(~)
            % No collision object initialization in this case
        end
        
        function sense(obj)
            start_pos = obj.start_pos;
            end_poses = obj.end_poses;
            for eidx = 1:length(end_poses)
                distance = obj.calculateDistanceBetweenPos(start_pos, end_poses(eidx, :));
                obj.value(eidx) = distance;
            end
        end
        
        function distance = calculateDistanceBetweenPos(~, pos1, pos2)
            x0 = pos1(1); y0 = pos1(2);
            x1 = pos2(1); y1 = pos2(2);
            distance = sqrt((x0-x1)^2 + (y0-y1)^2);
        end
        
        function collisionObject = getCollisionObject(obj)
            collisionObject = {obj.start_pos, obj.end_poses};
        end
        
        function visualObject = getVisualObject(obj)
            visualObject = {obj.start_pos, obj.end_poses};
        end
        
        function updateVisualObject(obj, idx, sx, sy, ex, ey)
            obj.start_pos = [sx, sy];
            obj.end_poses(idx, :) = [ex, ey];
        end
    end
end