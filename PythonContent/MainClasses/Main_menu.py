import pygame
import json
from PythonContent.MainClasses.UIElements import InputBox
from UIElements import TextRenderer, Button
import subprocess, os, sys
import sqlite3


class Menu:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        self.font_path = os.path.join("HomeVideo-Regular", "Assets/fonts/Game/HomeVideo-Regular.otf")
        self.font = pygame.font.Font('Assets/fonts/Game/HomeVideo-Regular.otf', 48)
        self.button_font = TextRenderer(self.font, color=(255, 255, 255))

        self.gameIcon = pygame.image.load("Assets/Sprites/icons/Icon33.png")
        pygame.display.set_caption("Templars of Elysium")

        self.surface = pygame.display.set_mode((800, 600))
        self.bgc = (45, 48, 44)
        pygame.display.set_icon(self.gameIcon)

    def run_menu(self):
        quit_button = Button("Quit", ((self.surface.get_width() - 220), 540), (200, 50), self.button_font)
        options_button = Button("Game Properties", ((self.surface.get_width() - 470), 480), (450, 50), self.button_font)
        instant_action_button = Button("Instant Action", ((self.surface.get_width() - 420), 420),
                                       (400, 50), self.button_font)
        campaign_button = Button("Campaign", ((self.surface.get_width() - 260), 360), (240, 50), self.button_font)
        game_logo = self.gameIcon.get_rect(center=(120, (self.surface.get_height() // 2) - 150))
        game_logo_sized = pygame.transform.scale(self.gameIcon, (256, 256))
        # Main loop
        running_menu = True
        while running_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running_menu = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if quit_button.is_clicked(event.pos):
                        running_menu = False
                    if instant_action_button.is_clicked(event.pos):
                        subprocess.Popen([sys.executable, "CombatGrid.py"])
                    if campaign_button.is_clicked(event.pos):
                        self.Run_CampaignMenu()
                        return

            self.surface.fill(self.bgc)

            name_render = TextRenderer(self.font, color=(255, 255, 255))
            name_render.draw_text(self.surface, "TEMPLARS OF ELYSIUM", (20, 20))

            # Draw the buttons
            self.surface.blit(game_logo_sized, game_logo)
            options_button.draw(self.surface)
            quit_button.draw(self.surface)
            instant_action_button.draw(self.surface)
            campaign_button.draw(self.surface)

            pygame.display.flip()

    def new_game_menu(self):
        create_button = Button("confirm", ((self.surface.get_width() - 280), 480), (260, 50),
                               self.button_font)
        name_ib = InputBox(((self.surface.get_width() - 480), 480,), (200, 50), self.button_font)
        back_btn = Button("return",((self.surface.get_width() - 220), 540), (200, 50), self.button_font)
        ng_run = True
        while ng_run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ng_run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if create_button.is_clicked(event.pos):
                        self.new_gameSQL(name_ib.get_name())
                        with open("GameData/menuD.txt", "w") as s:
                            f = name_ib.get_name()
                            s.write(f)
                        subprocess.Popen([sys.executable, "Global.py"])

                    elif back_btn.is_clicked(event.pos):
                        self.Run_CampaignMenu()
                        ng_run = False
                name_ib.handle_event(event)
            self.surface.fill(self.bgc)
            create_button.draw(self.surface)
            back_btn.draw(self.surface)
            name_ib.draw(self.surface)
            pygame.display.flip()

    def new_gameSQL(self, profile_name=None):
        connection = sqlite3.connect("GameData/players.db")
        self.cursor = connection.cursor()
        if profile_name is not None:
            profile_dir = "GameData/" + profile_name
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS player(
                        id INTEGER,
                        profile_dir TEXT NOT NULL,
                        profile_name TEXT NOT NULL)
                        ''')
            self.cursor.execute('SELECT COUNT(*) FROM player')
            counter = self.cursor.fetchone()[0]
            self.cursor.execute('''INSERT INTO player (id, profile_dir, profile_name) 
                                           VALUES (?, ?, ?)''', (counter, profile_dir, profile_name))
            connection.commit()

            # Create a new profile database
            profile = sqlite3.connect("GameData/Profiles/" + profile_name + ".db")
            pcursor = profile.cursor()
            pcursor.execute('''CREATE TABLE IF NOT EXISTS profile_data(
                        day INTEGER,
                        tech TEXT NOT NULL,
                        advances TEXT NOT NULL,
                        storage TEXT NOT NULL
                        )''')  # Closing parenthesis added here

            # Example of inserting data into the profile_data table
            character_data = {
  #              "day": 1,
  #              "tech": {"item1": "value1", "item2": "value2"},
  #              "advances": {"item1": 1, "item2": 2},
  #              "storage": {"item1": 10, "item2": 20}
            }

            # Convert dictionaries to JSON strings
  #          tech_json = json.dumps(character_data['tech'])
  #          advances_json = json.dumps(character_data['advances'])
  #          storage_json = json.dumps(character_data['storage'])

            # Insert the JSON strings into the table
  #          pcursor.execute('''
  #              INSERT INTO profile_data (day, tech, advances, storage) VALUES (?, ?, ?, ?)
  #          ''', (character_data['day'], tech_json, advances_json, storage_json))

            profile.commit()
            pcursor.close()
            profile.close()

        self.cursor.close()
        connection.close()
    def Run_CampaignMenu(self):
        new_btn = Button("New Game", ((self.surface.get_width() - 280), 480), (260, 50), self.button_font)
        back_btn = Button("Back", ((self.surface.get_width() - 220), 540), (200, 50), self.button_font)
        loadgame_btn = Button("Load Game", ((self.surface.get_width() - 280), 420), (260, 50), self.button_font)
        continue_btn = Button("Continue", ((self.surface.get_width() - 260), 360), (240, 50), self.button_font)
        typer_render = TextRenderer(self.font, color=(255, 255, 255))
        land_image = pygame.image.load("Assets/Sprites/Screens/landing.png")
        game_logo = land_image.get_rect(center=(120, (self.surface.get_height() // 2) - 150))
        game_logo_sized = pygame.transform.scale(land_image, (256, 256))

        running_menu = True
        while running_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running_menu = False
                if event.type == pygame.MOUSEBUTTONDOWN:  # Corrected line
                    if back_btn.is_clicked(event.pos):
                        self.run_menu()
                        running_menu = False  # Exit the campaign menu
                        return
                    if new_btn.is_clicked(event.pos):
                        self.new_game_menu()
                        return
                    #                subprocess.Popen([sys.executable, "Global.py"])
                    if loadgame_btn.is_clicked(event.pos):
                        print("Loading game...")
                    if continue_btn.is_clicked(event.pos):
                        print("Continuing game...")
            self.surface.fill(self.bgc)  # Clear the surface for the campaign menu
            new_btn.draw(self.surface)
            back_btn.draw(self.surface)
            loadgame_btn.draw(self.surface)
            continue_btn.draw(self.surface)
            self.surface.blit(game_logo_sized, game_logo)
            typer_render.draw_text(self.surface, "Campaign Mode", (20, 20))
            pygame.display.flip()
        pygame.quit()


if __name__ == "__main__":
    menu = Menu()
    menu.run_menu()
