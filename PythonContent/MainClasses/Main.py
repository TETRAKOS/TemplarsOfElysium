import pygame


pygame.init()


surface = pygame.display.set_mode((640,480))
bgc = (45,48,44)
running = True
surface.fill(bgc)
gameIcon = pygame.image.load("Assets/Sprites/icons/Icon33.png")
pygame.display.set_caption("Templars of Elysium")
pygame.display.set_icon(gameIcon)
pygame.display.flip()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
