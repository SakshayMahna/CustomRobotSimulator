classdef PELaserSensorActor < PEActor
    methods
        function obj = PELaserSensorActor(component)
            obj = obj@PEActor(component);
        end
        
        function step(obj, ~)
            sensor = obj.component;
            sensor.sense();
        end
    end
end

