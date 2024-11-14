import pygame
import sqlite3
import sys


class Shell:
    def __init__(self):
        pygame.init()
        self.gameIcon = pygame.image.load("Assets/Sprites/icons/Icon33.png")
        pygame.display.set_caption("Templars of Elysium - Planning")
        self.surface = pygame.display.set_mode((1024, 600))
        self.bgc = (45, 48, 44)
        pygame.display.set_icon(self.gameIcon)
        if len(sys.argv) > 1:
            self.profile = sys.argv[1]
            print(self.profile)
            self.main_screen()

    def main_screen(self):
        circle_map = pygame.image.load("Assets/Sprites/Backdrops/Circle.png")
        circle_image = circle_map.get_rect(center=(500, (self.surface.get_height() // 2) - 150))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.surface.fill(self.bgc)
            self.surface.blit(circle_map, circle_image)
            pygame.display.flip()

    def Run_shell(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.surface.fill(self.bgc)
            pygame.display.flip()
    def load_save(self):
        pass

class Town:
    pass
class District:
    pass

shell = Shell()
shell.Run_shell()