class PEActor:
    def __init__(self, component):
        self._component = component

    def step(self):
        pass

    def resolve_collision(self, dt):
        pass

    def get_collision_object(self):
        return self._component.get_collision_object()

class PERobotActor(PEActor):
    def step(self, dt):
        self._update_pose(dt)

    def resolve_collision(self, dt):
        self._update_pose(-1 * dt)
        
    def _update_pose(self, dt):
        robot = self._component        
        robot.move(dt)
        robot.update_collision_object()

class PEDistanceSensorActor(PEActor):
    def step(self, dt):
        sensor = self._component
        sensor.sense()

class PEGridActor(PEActor):
    def step(self, dt):
        pass
