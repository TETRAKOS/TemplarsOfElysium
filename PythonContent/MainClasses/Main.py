import pygame


pygame.init()


surface = pygame.display.set_mode((640,480))
bgc = (45,48,44)
running = True
surface.fill(bgc)
pygame.display.set_caption("Templars of Elysium")

pygame.display.flip()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False