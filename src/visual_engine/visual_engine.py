import pygame

class VisualEngine:
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._actors = []
    
    def add_actor(self, actor):
        self._actors.append(actor)

    def render(self):
        pass

class PygameVisualEngine(VisualEngine):
    def __init__(self, width = 1280, height = 720):
        super(PygameVisualEngine, self).__init__(width, height)
        pygame.init()

    def initialize(self):
        self._screen = pygame.display.set_mode((self._width, self._height))
        self._clock = pygame.time.Clock()
        self._dt = 0
        running = True

        return running

    def render(self):
        running = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        self._render_screen()
        self._dt = self._clock.tick(60) / 1000

        return running

    def _render_screen(self):
        screen = self._screen
        dt = self._dt
        actors = self._actors

        screen.fill("white")
        for actor in actors:
            actor.draw(screen)
        
        pygame.display.flip()

    def terminate(self):
        pygame.quit()