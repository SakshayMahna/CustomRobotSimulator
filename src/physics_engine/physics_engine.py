import pygame
from types import GeneratorType

class PhysicsEngine:
    def __init__(self, dt):
        self._dt = dt
        self._actors = []

    def add_actor(self, actor):
        self._actors.append(actor)

    def step(self):
        self._step_physics()
        self._collision_detection()
        self._collision_resolution()

    def _step_physics(self, dt):
        pass

    def _collision_detection(self):
        pass

    def _collision_resolution(self):
        pass


class PygamePhysicsEngine(PhysicsEngine):
    def _step_physics(self):
        dt = self._dt
        for actor in self._actors:
            actor.step(dt)

    def _collision_detection(self):
        [collision_objects, collision_map] = self._extract_collision_objects()
        collision_indices = set()
        for (cid, cobject) in zip(range(len(collision_objects)), collision_objects):
            indices = cobject.collidelistall(collision_objects)
            collision_indices.update([i for i in indices if i != cid])
        
        self._collision_objects = collision_objects
        self._collision_indices = collision_indices
        self._collision_map = collision_map

    def _extract_collision_objects(self):
        collision_objects = []
        collision_map = []
        for (actor_id, actor) in zip(range(len(self._actors)), self._actors):
            collision_object = actor.get_collision_object()
            if isinstance(collision_object, GeneratorType):
                collision_object_list = list(collision_object)
                collision_objects.extend(collision_object_list)
                collision_map.extend([actor_id] * len(collision_object_list))
            elif isinstance(collision_object, pygame.Rect):
                collision_objects.append(collision_object)
                collision_map.append(actor_id)
            else:
                continue

        return (collision_objects, collision_map)
    
    def _collision_resolution(self):
        dt = self._dt
        actors = self._actors
        collision_indices = self._collision_indices
        collision_map = self._collision_map
        for cindex in collision_indices:
            index = collision_map[cindex]
            actors[index].resolve_collision(dt)