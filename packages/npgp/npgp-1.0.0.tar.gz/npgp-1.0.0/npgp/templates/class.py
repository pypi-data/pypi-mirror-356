import pygame
import sys
from config import config


class Game:
    def __init__(self):
        pygame.init()

        # Screen setup
        self.screen = pygame.display.set_mode((config.screen.width, config.screen.height))
        pygame.display.set_caption(config.screen.title)

        # Clock and delta time
        self.clock = pygame.time.Clock()
        self.dt = 0

        # Game state
        self.running = True


    def run(self):
        while self.running:
            self.dt = self.clock.tick(config.fps_cap) / 1000

            self.handle_events()
            self.update()
            self.draw()

        pygame.quit()
        sys.exit()


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False


    def update(self):
        pass 


    def draw(self):
        self.screen.fill((0, 0, 0))
        pygame.display.flip()



if __name__ == "__main__":
    game = Game()
    game.run()
