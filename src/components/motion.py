from math import pi, sin, cos

class Pose:
    def __init__(self, x = 0, y = 0, theta = 0):
        self.x = x
        self.y = y
        self.theta = theta

class UnicycleModel:
    def __init__(self, init_pose):
        self._pose = init_pose

    def get_pose(self):
        return self._pose

    def move(self, v, w, dt):
        x = self._pose.x
        y = self._pose.y
        theta = self._pose.theta

        xdot = v * cos(theta);
        ydot = v * sin(theta);
        thetadot = w;

        x = x + xdot * dt;
        y = y + ydot * dt;
        theta = (theta + thetadot * dt) % (2*pi);

        self._pose.x = x 
        self._pose.y = y
        self._pose.theta = theta