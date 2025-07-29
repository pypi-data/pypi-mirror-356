import pygame, sys
from config import config


pygame.init()
screen = pygame.display.set_mode((config.screen.width, config.screen.height))
pygame.display.set_caption(config.screen.title)
clock = pygame.time.Clock()







running = True
while running:
    dt = clock.tick(config.fps_cap) / 1000
    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

    pygame.display.flip()
pygame.quit()