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
            self.mission_screen()
    def mission_screen(self):
        circle_map = pygame.image.load("Assets/Sprites/Backdrops/Circle.png")
        circle_image = circle_map.get_rect(center=(500, (self.surface.get_height() // 2)))
        raid_btn, tech_btn, info_btn,misc_btn = self.low_buttons_array("Mission")


    def low_buttons_array(self, state):
        raid_btn = Button("Mission", (50, 550), (225, 50), self.button_font, self.b_bgc,enabled=True)
        if state == "Mission":
            raid_btn.set_enabled(False)
        tech_btn = Button("Tech", (275, 550), (225, 50), self.button_font, self.b_bgc, enabled=True)
        if state == "Tech":
            tech_btn.set_enabled(False)
        units_btn = Button("Units", (500, 550), (225, 50), self.button_font, self.b_bgc, enabled=True)
        if state == "Units":
            units_btn.set_enabled(False)
        info_btn = Button("Info", (725, 550), (225, 50), self.button_font, self.b_bgc, enabled=True)
        if state == "Info":
            info_btn.set_enabled(False)
        return raid_btn,tech_btn,units_btn,info_btn
    # def Run_shell(self):
    #     running = True
    #     while running:
    #         for event in pygame.event.get():
    #              if event.type == pygame.QUIT:
    #                  running = False
    #              if event.type == pygame.MOUSEBUTTONDOWN:
    #                  if
    #         self.surface.fill(self.bgc)
    #         pygame.display.flip()
    # def load_save(self):
    #     pass

class Town:
    pass
class District:
    pass

shell = Shell()
