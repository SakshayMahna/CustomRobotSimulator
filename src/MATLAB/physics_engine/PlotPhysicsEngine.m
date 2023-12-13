classdef PlotPhysicsEngine < PhysicsEngine
    methods (Access = private)
        function stepPhysics(obj)
            dt = obj.dt;
            for i = 1:numel(obj.actors)
                obj.actors{i}.step(dt);
            end
        end
        
        function collisionDetection(obj)
            [collisionObjects, collisionMap] = obj.extractCollisionObjects();
            collisionIndices = containers.Map('KeyType','double','ValueType','logical');
            for cid = 1:numel(collisionObjects)
                indices = collidelistall(collisionObjects{cid}, collisionObjects);
                indices(indices == cid) = [];
                collisionIndices = union(collisionIndices, indices);
            end
            obj.collisionObjects = collisionObjects;
            obj.collisionIndices = keys(collisionIndices);
            obj.collisionMap = collisionMap;
        end
        
        function [collisionObjects, collisionMap] = extractCollisionObjects(obj)
            collisionObjects = {};
            collisionMap = [];
            for actorId = 1:numel(obj.actors)
                collisionObject = obj.actors{actorId}.getCollisionObject();
                if iscell(collisionObject)
                    collisionObjects = [collisionObjects, collisionObject];
                    collisionMap = [collisionMap, repmat(actorId, 1, numel(collisionObject))];
                elseif isa(collisionObject, 'Rectangle')
                    collisionObjects{end+1} = collisionObject;
                    collisionMap(end+1) = actorId;
                else
                    continue;
                end
            end
        end
        
        function collisionResolution(obj)
            dt = obj.dt;
            actors = obj.actors;
            collisionIndices = obj.collisionIndices;
            collisionMap = obj.collisionMap;
            for cindex = 1:numel(collisionIndices)
                index = collisionMap(collisionIndices(cindex));
                actors{index}.resolveCollision(dt);
            end
        end
    end
end