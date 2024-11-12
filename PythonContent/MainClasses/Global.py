import pygame

class Shell:
    def __init__(self):
        pygame.init()
        self.gameIcon = pygame.image.load("Assets/Sprites/icons/Icon33.png")
        pygame.display.set_caption("Templars of Elysium - Planning")
        self.surface = pygame.display.set_mode((800, 600))
        self.bgc = (45, 48, 44)
        pygame.display.set_icon(self.gameIcon)
    def Run_shell(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.surface.fill(self.bgc)
            pygame.display.flip()
    pass
class Town():
    pass
class District():
    pass

shell = Shell()
shell.Run_shell()