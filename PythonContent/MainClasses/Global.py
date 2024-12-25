import pygame
import sys
from PythonContent.MainClasses.UIElements import ImageButton
from UIElements import Button, TextRenderer

class Shell:
    def __init__(self, surface, font, font_small, gameIcon):
        self.surface = surface
        self.font = font
        self.font_small = font_small
        self.gameIcon = gameIcon
        self.bgc = (45, 48, 44)
        self.b_bgc = (35, 38, 34)
        self.selected_fcl = None
        pygame.display.set_icon(self.gameIcon)
        if len(sys.argv) > 1:
            self.profile = sys.argv[1]
            print(self.profile)
        else:
            print("No profile specified")

    def mission_screen(self):
        factory_d = pygame.image.load("Assets/Sprites/Entities/Buildings/Factory/Factory_default.png")
        factory_h = pygame.image.load("Assets/Sprites/Entities/Buildings/Factory/Factory_highlighted.png")
        factory_s = pygame.image.load("Assets/Sprites/Entities/Buildings/Factory/Factory_selected.png")
        admin_d = pygame.image.load("Assets/Sprites/Entities/Buildings/Administration/admin_default.png")
        admin_h = pygame.image.load("Assets/Sprites/Entities/Buildings/Administration/admin_highlight.png")
        admin_s = pygame.image.load("Assets/Sprites/Entities/Buildings/Administration/admin_selected.png")
        gardens_d = pygame.image.load("Assets/Sprites/Entities/Buildings/Gardens/Gardens_default.png")
        gardens_h = pygame.image.load("Assets/Sprites/Entities/Buildings/Gardens/Gardens_highlight.png")
        gardens_s = pygame.image.load("Assets/Sprites/Entities/Buildings/Gardens/Gardens_selected.png")
        tower_countur = pygame.image.load("Assets/Sprites/Entities/Buildings/Tower/tower_back.png")
        tower_cb = tower_countur.get_rect(center=(500, (self.surface.get_height() // 2)))
        command_image = pygame.image.load("Assets/Sprites/Entities/Buildings/Tower/Tower.png")
        command_pl = (526,59)
        circle_map = pygame.image.load("Assets/Sprites/Backdrops/Circle.png")
        circle_image = circle_map.get_rect(center=(500, (self.surface.get_height() // 2)))
        raid_main = TextRenderer(self.font, color=(255, 255, 255))
        raid_description=TextRenderer(self.font_small, color=(255, 255, 255))
        prep_raid_btn = Button("Prepare for intrusion", (50, 450), (300, 75), self.font, enabled=False)

        raid_btn, tech_btn, info_btn,misc_btn = self.low_buttons_array("Mission")
        save_btn, load_btn, options_btn, quit_btn = self.high_buttons_array()
        haz1_bld = ImageButton(factory_d, factory_h,factory_s,(500,116),(122,292))
        haz2_bld = ImageButton(admin_d, admin_h,admin_s,(412,46),(170,260))
        haz3_bld = ImageButton(gardens_d, gardens_h, gardens_s,(380,200),(162,259))
        raid_mt = "Select facility for intrusion"
        raid_subt = ("Different facilities store different"
                     " types of resources, choose as needed")
        menu_running = True
        while menu_running:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu_running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if raid_btn.is_clicked(event.pos):
                            print("Raid Button Clicked")
                    elif tech_btn.is_clicked(event.pos):
                            self.tech_menu()
                            menu_running = False

                    elif info_btn.is_clicked(event.pos):
                            print("Info Button Clicked")
                    elif misc_btn.is_clicked(event.pos):
                            print("Misc Button Clicked")
                    elif haz1_bld.is_clicked(event.pos):
                         haz1_bld.in_focus(True)
                         haz2_bld.in_focus(False),haz3_bld.in_focus(False)
                         print("Factory Button Clicked")
                         raid_mt = "Factory"
                         raid_subt = ("Production part of the Tower, storing mechanical components and engineering "
                                      "blueprints, occupied by the Cult of the Hammer, high-tech aggressive combatants,"
                                      "high environment hazards, mechanical threats")
                         self.selected_fcl = "Factory"
                    elif haz2_bld.is_clicked(event.pos):
                        haz2_bld.in_focus(True)
                        haz3_bld.in_focus(False), haz1_bld.in_focus(False)
                        print("Admin Button Clicked")
                        raid_mt = "Administration"
                        raid_subt = ("Control part of the Tower, managing the Tower's resources, stores a lot of "
                                     "important administrative data, signs of scavengers and mutants, automated defense systems,"
                                      "low-tech nature of office environment suggest low chance of environment hazards")
                        self.selected_fcl = "Administration"
                    elif haz3_bld.is_clicked(event.pos):
                        haz3_bld.in_focus(True)
                        haz2_bld.in_focus(False), haz1_bld.in_focus(False)
                        print("Gardens Button Clicked")
                        raid_mt = "Gardens"
                        raid_subt = ("Gardens part of the Tower, stores food, water, and other necessary resources,"
                                     "biological hazard, occasional burst of mutated flora and fauna "
                                     "spreads all over different sections of tower, miriade of semi-sentient hostile "
                                     "entities, high-tech nature of the gardens and distorted nature suggests"
                                     " that this is a hazardous environment")
                        self.selected_fcl = "Gardens"
                    elif save_btn.is_clicked(event.pos):
                        print("Save Button Clicked")
                    elif load_btn.is_clicked(event.pos):
                        print("Load Button Clicked")
                    elif prep_raid_btn.is_clicked(event.pos):
                        print("Preparation for Raid Button Clicked")
                        return "game"  # Switch to the game state
                    elif options_btn.is_clicked(event.pos):
                        print("Options Button Clicked")
                    elif quit_btn.is_clicked(event.pos):
                        menu_running = False

                haz1_bld.update(mouse_pos)
                haz2_bld.update(mouse_pos)
                haz3_bld.update(mouse_pos)
                self.surface.fill(self.bgc)
                prep_raid_btn.set_enabled(True if self.selected_fcl != None else False)
                prep_raid_btn.update_text("Prepare for intrusion" if self.selected_fcl!= None else "Select the facility")
                self.surface.blit(tower_countur, tower_cb)
                raid_btn.draw(self.surface), tech_btn.draw(self.surface),info_btn.draw(self.surface),misc_btn.draw(self.surface)
                save_btn.draw(self.surface),load_btn.draw(self.surface), options_btn.draw(self.surface), quit_btn.draw(self.surface)
                haz1_bld.draw(self.surface)
                haz2_bld.draw(self.surface)
                haz3_bld.draw(self.surface)
                prep_raid_btn.draw(self.surface)

                self.surface.blit(command_image, command_pl)
                raid_main.draw_text(self.surface,raid_mt,(20,15),800)
                raid_description.draw_text(self.surface,raid_subt, (20,60),380)
                pygame.display.flip()

        return "shell"  # Return to the shell state if the loop exits

    def high_buttons_array(self):
        save_btn = Button("Save", (620, 0), (100, 25), self.font_small, self.b_bgc,)
        load_btn = Button("Load", (720, 0), (100, 25), self.font_small, self.b_bgc,)
        options_btn = Button("Options", (820, 0), (100, 25), self.font_small, self.b_bgc,)
        quit_btn = Button("Quit", (920, 0), (100, 25), self.font_small, self.b_bgc,)
        return save_btn, load_btn, options_btn, quit_btn

    def low_buttons_array(self, state):
        raid_btn = Button("Mission", (50, 550), (225, 50), self.font, self.b_bgc,enabled=True)
        if state == "Mission":
            raid_btn.set_enabled(False)
        tech_btn = Button("Tech", (275, 550), (225, 50), self.font, self.b_bgc, enabled=True)
        if state == "Tech":
            tech_btn.set_enabled(False)
        units_btn = Button("Units", (500, 550), (225, 50), self.font, self.b_bgc, enabled=True)
        if state == "Units":
            units_btn.set_enabled(False)
        info_btn = Button("Info", (725, 550), (225, 50), self.font, self.b_bgc, enabled=True)
        if state == "Info":
            info_btn.set_enabled(False)
        return raid_btn,tech_btn,units_btn,info_btn

    def tech_menu(self):
        raid_b, tech_b, gear_b, info_b = self.low_buttons_array('Tech')
        t_running=True
        while t_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    t_running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if raid_b.is_clicked(event.pos):
                        self.mission_screen()
                        t_running = False
                    elif tech_b.is_clicked(event.pos):
                        print("none")
                    elif gear_b.is_clicked(event.pos):
                        print("Units")
                    elif info_b.is_clicked(event.pos):
                        print("info")
            self.surface.fill(self.bgc)
            raid_b.draw(self.surface), tech_b.draw(self.surface), gear_b.draw(self.surface), info_b.draw(
                self.surface)
            pygame.display.flip()