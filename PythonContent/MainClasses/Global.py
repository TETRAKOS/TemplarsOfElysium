import json

import pygame
import sys
from PythonContent.MainClasses.UIElements import ImageButton
from UIElements import Button, TextRenderer
import sqlite3

class Technology:
    def __init__(self, name, dependencies=None, position=(50, 50)):
        self.name = name
        self.dependencies = dependencies if dependencies else []
        self.position = position
        self.researched = False
        self.tech_tree = None

    def set_tech_tree(self, tech_tree):
        self.tech_tree = tech_tree

    def can_research(self):
        return all(self.tech_tree[dep].researched for dep in self.dependencies)

tech_tree = {
    "Survival equipment": Technology("Survival equipment", None, position=(25, 250)),
    "Basic Firearms": Technology("Basic Firearms", dependencies=["Survival equipment"], position=(275, 250)),
    "Buckshot": Technology("Buckshot", dependencies=["Basic Firearms"], position=(425, 400)),
    "Automatics": Technology("Automatics", dependencies=["Basic Firearms"], position=(425, 100)),
    "Vitals stabilizers": Technology("Vitals stabilizers", None, position=(50, 450)),
    "Laser": Technology("Laser", dependencies=["Automatics", "Buckshot"], position=(625, 250)),
    "Advanced Medicine": Technology("Advanced Medicine", dependencies=["Vitals stabilizers", "Laser"], position=(800, 450)),
}

for tech in tech_tree.values():
    tech.set_tech_tree(tech_tree)

class TechTreeUI:
    def __init__(self, surface, font, tech_tree, db_connection, db_cursor):
        self.surface = surface
        self.font = font
        self.tech_tree = tech_tree
        self.buttons = {}
        self.db_connection = db_connection
        self.db_cursor = db_cursor
        self.create_buttons()
        self.load_researched_technologies()

    def load_researched_technologies(self):
        try:
            self.db_cursor.execute("SELECT tech FROM profile_data")
            result = self.db_cursor.fetchone()
            if result and result[0]:
                researched_techs = result[0].split(',')
                for tech_name in researched_techs:
                    if tech_name in self.tech_tree:
                        self.tech_tree[tech_name].researched = True
                self.update_buttons()
        except sqlite3.Error as e:
            print(f"Error loading researched technologies: {e}")

    def save_researched_technologies(self):
        researched_techs = ','.join([tech.name for tech in self.tech_tree.values() if tech.researched])
        try:
            self.db_cursor.execute("UPDATE profile_data SET tech = ?", (researched_techs,))
            self.db_connection.commit()
            print("Researched technologies saved successfully.")
        except sqlite3.Error as e:
            print(f"Error saving researched technologies: {e}")

    def create_buttons(self):
        button_width = 175
        button_height = 75
        for tech in self.tech_tree.values():
            button = Button(tech.name, tech.position, (button_width, button_height), self.font, enabled=tech.can_research(),
                            disabled_color=(55, 55, 55), selected_color=(0, 255, 0))
            self.buttons[tech.name] = button

    def draw(self):
        for button in self.buttons.values():
            button.draw(self.surface)
        self.draw_lines()

    def draw_lines(self):
        for tech_name, tech in self.tech_tree.items():
            for dep_name in tech.dependencies:
                dep = self.tech_tree[dep_name]
                start_pos = self.get_button_center(self.buttons[dep_name])
                end_pos = self.get_button_center(self.buttons[tech_name])
                pygame.draw.line(self.surface, (125, 175, 125), start_pos, end_pos, 2)

    def get_button_center(self, button):
        return (button.position[0] + button.size[0] // 2, button.position[1] + button.size[1] // 2)

    def handle_event(self, event):
        for tech_name, button in self.buttons.items():
            if button.is_clicked(event.pos):
                tech = self.tech_tree[tech_name]
                if tech.can_research() and not tech.researched:
                    tech.researched = True
                    self.update_buttons()
                    print(f"Researched {tech.name}")
                    self.save_researched_technologies()
                    self.add_to_storage(tech.name)

    def update_buttons(self):
        for tech_name, button in self.buttons.items():
            tech = self.tech_tree[tech_name]
            button.set_enabled(tech.can_research() and not tech.researched)
            if tech.researched:
                button.selected = True

    def add_to_storage(self, tech_name):
        with open('Assets/dicts/tech_tree.js', 'r') as file:
            tech_table = json.load(file)
        try:
            print(tech_name)
            item_id = tech_table.get(tech_name)
            print(item_id)
            print(f"Item ID for {tech_name}: {item_id}")
            if item_id:
                self.db_cursor.execute("SELECT storage FROM profile_data")
                storage_result = self.db_cursor.fetchone()
                storage_items = storage_result[0].split(',') if storage_result[0] else []
                storage_items.append(item_id)
                storage_str = ','.join(storage_items)
                self.db_cursor.execute("UPDATE profile_data SET storage = ?", (storage_str,))
                self.db_connection.commit()
                print(f"Added {tech_name} to storage.")
            else:
                print(f"Item ID for {tech_name} not found.")
        except sqlite3.Error as e:
            print(f"Error adding item to storage: {e}")
class Shell:
    def __init__(self, surface, font, font_small, gameIcon, screen, save):
        self.save_data = save[1]
        self.surface = surface
        self.font = font
        self.screen = screen
        self.font_small = font_small
        self.gameIcon = gameIcon
        self.bgc = (45, 48, 44)
        self.b_bgc = (35, 38, 34)
        self.selected_fcl = None
        pygame.display.set_icon(self.gameIcon)
        print(self.save_data)
        self.db_connection = None
        self.db_cursor = None
        self.profile_data = None
        self.initialize_database()
        self.tech_tree_ui = None

    def initialize_database(self):
        try:
            self.db_connection = sqlite3.connect(self.save_data)
            self.db_cursor = self.db_connection.cursor()
            self.fetch_profile_data()
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def fetch_profile_data(self):
        try:
            self.db_cursor.execute("SELECT * FROM profile_data")
            self.profile_data = self.db_cursor.fetchall()
            print("Profile data fetched successfully:", self.profile_data)

            # Check if the 'day' field is empty and update it if necessary
            if not self.profile_data:
                self.db_cursor.execute("INSERT INTO profile_data (day, tech, advances, storage, gear) VALUES (?, ?, ?, ?, ?)",
                                       (1, '', '', '', ''))
                self.db_connection.commit()
                print("Default data inserted successfully.")
            else:
                for row in self.profile_data:
                    if row[0] is None:  # Assuming 'day' is the first column
                        self.db_cursor.execute("UPDATE profile_data SET day = ? WHERE rowid = ?", (1, row[0]))
                        self.db_connection.commit()
                        print("Updated 'day' field to 1.")

        except sqlite3.Error as e:
            print(f"Error fetching profile data: {e}")

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
        tower_counter = pygame.image.load("Assets/Sprites/Backdrops/Circle.png")
        tower_cb = tower_counter.get_rect(center=(500, (self.surface.get_height() // 2)))
        command_image = pygame.image.load("Assets/Sprites/Entities/Buildings/Tower/Tower.png")
        command_pl = (526, 59)
        circle_map = pygame.image.load("Assets/Sprites/Backdrops/Circle.png")
        circle_image = circle_map.get_rect(center=(500, (self.surface.get_height() // 2)))
        raid_main = TextRenderer(self.font, color=(255, 255, 255))
        raid_description = TextRenderer(self.font_small, color=(255, 255, 255))
        prep_raid_btn = Button("Prepare for Intrusion", (50, 450), (300, 75), self.font, enabled=False)

        raid_btn, tech_btn, units_btn, info_btn = self.low_buttons_array("Mission")
       # save_btn, load_btn, options_btn, quit_btn = self.high_buttons_array()
        haz1_bld = ImageButton(factory_d, factory_h, factory_s, (500, 116), (122, 292))
        haz2_bld = ImageButton(admin_d, admin_h, admin_s, (412, 46), (170, 260))
        haz3_bld = ImageButton(gardens_d, gardens_h, gardens_s, (380, 200), (162, 259))
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
                        pass
                    elif tech_btn.is_clicked(event.pos):
                        self.tech_menu()
                        menu_running = False
                    elif units_btn.is_clicked(event.pos):
                        self.inventory_screen()
                        menu_running = False
                        print("Units Button Clicked")
                    elif info_btn.is_clicked(event.pos):
                        pass
                        # menu_running = False
                    elif haz1_bld.is_clicked(event.pos):
                        haz1_bld.in_focus(True)
                        haz2_bld.in_focus(False)
                        haz3_bld.in_focus(False)
                        print("Factory Button Clicked")
                        raid_mt = "Factory"
                        raid_subt = ("Production part of the Tower, storing mechanical components and engineering "
                                      "blueprints, occupied by the Cult of the Hammer, high-tech aggressive combatants,"
                                      "high environment hazards, mechanical threats")
                        self.selected_fcl = "Factory"
                    elif haz2_bld.is_clicked(event.pos):
                        haz2_bld.in_focus(True)
                        haz3_bld.in_focus(False)
                        haz1_bld.in_focus(False)
                        print("Admin Button Clicked")
                        raid_mt = "Administration"
                        raid_subt = ("Control part of the Tower, managing the Tower's resources, stores a lot of "
                                     "important administrative data, signs of scavengers and mutants, automated defense systems,"
                                     "low-tech nature of office environment suggests low chance of environment hazards")
                        self.selected_fcl = "Administration"
                    elif haz3_bld.is_clicked(event.pos):
                        haz3_bld.in_focus(True)
                        haz2_bld.in_focus(False)
                        haz1_bld.in_focus(False)
                        print("Gardens Button Clicked")
                        raid_mt = "Gardens"
                        raid_subt = ("Gardens part of the Tower, stores food, water, and other necessary resources,"
                                     "biological hazard, occasional burst of mutated flora and fauna "
                                     "spreads all over different sections of tower, miriad of semi-sentient hostile "
                                     "entities, high-tech nature of the gardens and distorted nature suggests"
                                     " that this is a hazardous environment")
                        self.selected_fcl = "Gardens"
                    # elif save_btn.is_clicked(event.pos):
                    #     print("Save Button Clicked")
                    # elif load_btn.is_clicked(event.pos):
                    #     print("Load Button Clicked")
                    elif prep_raid_btn.is_clicked(event.pos):
                        print("Preparation for Raid Button Clicked")
                        self.screen.search_new_state("game")
                        menu_running = False
                    # elif options_btn.is_clicked(event.pos):
                    #     print("Options Button Clicked")
                    # elif quit_btn.is_clicked(event.pos):
                    #     menu_running = False

                haz1_bld.update(mouse_pos)
                haz2_bld.update(mouse_pos)
                haz3_bld.update(mouse_pos)
                self.surface.fill(self.bgc)
                prep_raid_btn.set_enabled(True if self.selected_fcl is not None else False)
                prep_raid_btn.update_text("Prepare for Intrusion" if self.selected_fcl is not None else "Select the facility")
                self.surface.blit(tower_counter, tower_cb)
                raid_btn.draw(self.surface)
                tech_btn.draw(self.surface)
                units_btn.draw(self.surface)
                info_btn.draw(self.surface)
                # save_btn.draw(self.surface)
                # load_btn.draw(self.surface)
                # options_btn.draw(self.surface)
                # quit_btn.draw(self.surface)
                haz1_bld.draw(self.surface)
                haz2_bld.draw(self.surface)
                haz3_bld.draw(self.surface)
                prep_raid_btn.draw(self.surface)

                self.surface.blit(command_image, command_pl)
                raid_main.draw_text(self.surface, raid_mt, (20, 15), 800)
                raid_description.draw_text(self.surface, raid_subt, (20, 60), 380)
                pygame.display.flip()

        return "shell"

    def high_buttons_array(self):
        save_btn = Button("Save", (620, 0), (100, 25), self.font_small, self.b_bgc)
        load_btn = Button("Load", (720, 0), (100, 25), self.font_small, self.b_bgc)
        options_btn = Button("Options", (820, 0), (100, 25), self.font_small, self.b_bgc)
        quit_btn = Button("Quit", (920, 0), (100, 25), self.font_small, self.b_bgc)
        return save_btn, load_btn, options_btn, quit_btn

    def low_buttons_array(self, state):
        raid_btn = Button("Mission", (50, 550), (225, 50), self.font, self.b_bgc, enabled=True)
        if state == "Mission":
            raid_btn.set_enabled(False)
        tech_btn = Button("Tech", (275, 550), (225, 50), self.font, self.b_bgc, enabled=True)
        if state == "Tech":
            tech_btn.set_enabled(False)
        units_btn = Button("Gear", (500, 550), (225, 50), self.font, self.b_bgc, enabled=True)
        if state == "Gear":
            units_btn.set_enabled(False)
        info_btn = Button("Info", (725, 550), (225, 50), self.font, self.b_bgc, enabled=True)
        if state == "Info":
            info_btn.set_enabled(False)
        return raid_btn, tech_btn, units_btn, info_btn

    def tech_menu(self):
        tech_font = pygame.font.Font('Assets/fonts/Game/HomeVideo-Regular.otf', 20)
        self.tech_tree_ui = TechTreeUI(self.surface, tech_font, tech_tree, self.db_connection, self.db_cursor)
        t_running = True
        raid_btn, tech_btn, gear_btn, misc_btn = self.low_buttons_array("Tech")
        while t_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    t_running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.tech_tree_ui.handle_event(event)
                    if event.button == 3:
                        self.mission_screen()
                        t_running = False
                    if raid_btn.is_clicked(event.pos):
                        self.mission_screen()
                        t_running = False
                    elif tech_btn.is_clicked(event.pos):
                        self.tech_menu()
                        t_running = False
                    elif gear_btn.is_clicked(event.pos):
                        self.inventory_screen()
                        t_running = False
                    elif misc_btn.is_clicked(event.pos):
                        print("Misc Button Clicked")

            self.surface.fill(self.bgc)
            self.tech_tree_ui.draw()
            raid_btn.draw(self.surface)
            tech_btn.draw(self.surface)
            gear_btn.draw(self.surface)
            misc_btn.draw(self.surface)
            pygame.display.flip()
    def inventory_screen(self):
        self.inventory_manager = InventoryManager(self.surface, self.font, self.db_connection, self.db_cursor)
        raid_btn, tech_btn, units_btn, info_btn = self.low_buttons_array("Gear")
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.inventory_manager.handle_event(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if raid_btn.is_clicked(event.pos):
                        self.mission_screen()
                        running = False
                    elif tech_btn.is_clicked(event.pos):
                        self.tech_menu()
                        running = False
                    elif units_btn.is_clicked(event.pos):
                        self.inventory_screen()
                        pass
                    elif info_btn.is_clicked(event.pos):
                        pass
                        # menu_running = False

            self.surface.fill(self.bgc)
            self.inventory_manager.draw()
            raid_btn.draw(self.surface)
            tech_btn.draw(self.surface)
            units_btn.draw(self.surface)
            info_btn.draw(self.surface)
            pygame.display.flip()

        return "shell"


class InventoryManager:
    def __init__(self, surface, font, db_connection, db_cursor):
        self.surface = surface
        self.font = font
        self.db_connection = db_connection
        self.db_cursor = db_cursor
        self.gear_items = []
        self.storage_items = []
        self.load_inventory()
        self.create_buttons()

    def load_inventory(self):
        try:
            self.db_cursor.execute("SELECT gear, storage FROM profile_data")
            result = self.db_cursor.fetchone()
            if result:
                self.gear_items = self.clean_inventory_data(result[0].split(',')) if result[0] else []
                self.storage_items = self.clean_inventory_data(result[1].split(',')) if result[1] else []
        except sqlite3.Error as e:
            print(f"Error loading inventory: {e}")

    def clean_inventory_data(self, items):
        cleaned_items = []
        for item in items:
            item = item.strip()  # Remove any leading/trailing whitespace
            if item.startswith('[') and item.endswith(']'):
                item = item[1:-1]  # Remove brackets
            cleaned_items.append(item)
        return cleaned_items

    def save_inventory(self):
        gear_str = ','.join(self.gear_items)
        storage_str = ','.join(self.storage_items)
        try:
            self.db_cursor.execute("UPDATE profile_data SET gear = ?, storage = ?", (gear_str, storage_str))
            self.db_connection.commit()
            print("Inventory saved successfully.")
        except sqlite3.Error as e:
            print(f"Error saving inventory: {e}")

    def create_buttons(self):
        self.gear_buttons = []
        self.storage_buttons = []
        button_width = 150
        button_height = 50
        y_offset = 50

        for item in self.gear_items:
            button = Button(item, (50, y_offset), (button_width, button_height), self.font)
            self.gear_buttons.append(button)
            y_offset += 60

        y_offset = 50
        for item in self.storage_items:
            button = Button(item, (300, y_offset), (button_width, button_height), self.font)
            self.storage_buttons.append(button)
            y_offset += 60

    def draw(self):
        for button in self.gear_buttons:
            button.draw(self.surface)
        for button in self.storage_buttons:
            button.draw(self.surface)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.gear_buttons:
                if button.is_clicked(event.pos):
                    item = button.text
                    self.gear_items.remove(item)
                    self.storage_items.append(item)
                    self.create_buttons()
                    self.save_inventory()
                    print(f"Moved {item} from gear to storage")

            for button in self.storage_buttons:
                if button.is_clicked(event.pos):
                    item = button.text
                    self.storage_items.remove(item)
                    self.gear_items.append(item)
                    self.create_buttons()
                    self.save_inventory()
                    print(f"Moved {item} from storage to gear")
