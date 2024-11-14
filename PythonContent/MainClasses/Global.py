import pygame
#import sqlite3
import sys
from UIElements import Button, TextRenderer


class Shell:
    def __init__(self):
        pygame.init()
        self.font = pygame.font.Font('Assets/fonts/Game/HomeVideo-Regular.otf', 32)
        self.button_font = TextRenderer(self.font, color=(255, 255, 255))
        self.gameIcon = pygame.image.load("Assets/Sprites/icons/Icon33.png")
        pygame.display.set_caption("Templars of Elysium - Planning")
        self.surface = pygame.display.set_mode((1024, 600))
        self.bgc = (45, 48, 44)
        self.b_bgc = (35, 38, 34)
        pygame.display.set_icon(self.gameIcon)
        if len(sys.argv) > 1:
            self.profile = sys.argv[1]
            print(self.profile)
            self.main_screen()

    def main_screen(self):
        raid_btn = Button("Raid", (50, 550), (225,50), self.button_font, self.b_bgc)
        tech_btn = Button("Tech", (275, 550), (225, 50), self.button_font, self.b_bgc)
        info_btn = Button("Info", (500, 550), (225, 50), self.button_font, self.b_bgc)
        misc_btn = Button("Misc", (725, 550), (225, 50), self.button_font, self.b_bgc)
        circle_map = pygame.image.load("Assets/Sprites/Backdrops/Circle.png")
        circle_image = circle_map.get_rect(center=(500, (self.surface.get_height() // 2)))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.surface.fill(self.bgc)
            self.surface.blit(circle_map, circle_image)
            raid_btn.draw(self.surface)
            tech_btn.draw(self.surface)
            info_btn.draw(self.surface)
            misc_btn.draw(self.surface)
            pygame.display.flip()

    # def Run_shell(self):
    #     running = True
    #     while running:
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 running = False
    #         self.surface.fill(self.bgc)
    #         pygame.display.flip()
    # def load_save(self):
    #     pass

class Town:
    pass
class District:
    pass

shell = Shell()
