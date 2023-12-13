classdef Motion < handle    
    properties(Access = private)
        pose;
    end
    
    methods
        function obj = Motion(init_pose)
            obj.pose = init_pose;
        end
        
        function pose = getPose(obj)
            pose = obj.pose;
        end

        function move(obj, v, w, dt)
            x = obj.pose.x;
            y = obj.pose.y;
            theta = obj.pose.theta;

            xdot = v * cos(theta);
            ydot = v * sin(theta);
            thetadot = w;

            x = x + xdot * dt;
            y = y + ydot * dt;
            theta = mod(theta + thetadot * dt, 2*pi);

            obj.pose.x = x;
            obj.pose.y = y;
            obj.pose.theta = theta;
        end
    end
end

