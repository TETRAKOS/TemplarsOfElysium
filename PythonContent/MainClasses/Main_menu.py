import pygame
from UIElements import TextRenderer, Button, InputBox
import subprocess, os, sys
import sqlite3

class Menu:
    def __init__(self, surface):
        pygame.init()
        pygame.mixer.init()
        self.surface = surface
        self.font_path = os.path.join("HomeVideo-Regular", "Assets/fonts/Game/HomeVideo-Regular.otf")
        self.font = pygame.font.Font('Assets/fonts/Game/HomeVideo-Regular.otf', 48)
        self.button_font = TextRenderer(self.font, color=(255, 255, 255))
        self.music = pygame.mixer.Sound("Assets/Sound/Music/TE_menu.wav")
        self.music.set_volume(0.4)
        self.music.play(-1)

        self.gameIcon = pygame.image.load("Assets/Sprites/icons/Icon33.png")
        pygame.display.set_caption("Templars of Elysium")

        self.bgc = (45, 48, 44)
        pygame.display.set_icon(self.gameIcon)

    def run_menu(self):
        quit_button = Button("Quit", ((self.surface.get_width() - 220), 540), (200, 50), self.font, enabled=True)
        options_button = Button("Game Properties", ((self.surface.get_width() - 470), 480), (450, 50), self.font,
                                enabled=True)
        instant_action_button = Button("Instant Action", ((self.surface.get_width() - 420), 420), (400, 50),
                                       self.font, enabled=True)
        campaign_button = Button("Campaign", ((self.surface.get_width() - 260), 360), (240, 50), self.font,
                                 enabled=True)
        game_logo = self.gameIcon.get_rect(center=(120, (self.surface.get_height() // 2) - 150))
        game_logo_sized = pygame.transform.scale(self.gameIcon, (256, 256))
        running_menu = True
        while running_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if quit_button.is_clicked(event.pos):
                        return "quit"
                    if instant_action_button.is_clicked(event.pos):
                        return "game"  # Switch to the game state
                    if campaign_button.is_clicked(event.pos):
                        return self.Run_CampaignMenu()

            self.surface.fill(self.bgc)

            name_render = TextRenderer(self.font, color=(255, 255, 255))
            name_render.draw_text(self.surface, "TEMPLARS OF ELYSIUM", (20, 20), 2000)

            # Draw the buttons
            self.surface.blit(game_logo_sized, game_logo)
            options_button.draw(self.surface)
            quit_button.draw(self.surface)
            instant_action_button.draw(self.surface)
            campaign_button.draw(self.surface)

            pygame.display.flip()

        return "menu"

    def new_game_menu(self):
        create_button = Button("confirm", ((self.surface.get_width() - 280), 480), (260, 50), self.font,
                               enabled=True)
        name_ib = InputBox(((self.surface.get_width() - 480), 480,), (200, 50), self.font)
        back_btn = Button("return", ((self.surface.get_width() - 220), 540), (200, 50), self.font, enabled=True)
        ng_run = True
        while ng_run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if create_button.is_clicked(event.pos):
                        self.new_gameSQL(name_ib.get_name())
                        return "game"  # Switch to the game state
                    elif back_btn.is_clicked(event.pos):
                        return self.Run_CampaignMenu()
                name_ib.handle_event(event)
            self.surface.fill(self.bgc)
            create_button.draw(self.surface)
            back_btn.draw(self.surface)
            name_ib.draw(self.surface)
            pygame.display.flip()

        return "menu"

    def new_gameSQL(self, profile_name=None):
        connection = sqlite3.connect("GameData/players.db")
        self.cursor = connection.cursor()
        if profile_name is not None:
            profile_dir = "GameData/" + profile_name + ".db"
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
                        )''')

            profile.commit()
            pcursor.close()
            profile.close()

        self.cursor.close()
        connection.close()

    def Run_CampaignMenu(self):
        new_btn = Button("New Game", ((self.surface.get_width() - 280), 480), (260, 50), self.font, enabled=True)
        back_btn = Button("Back", ((self.surface.get_width() - 220), 540), (200, 50), self.font, enabled=True)
        loadgame_btn = Button("Load Game", ((self.surface.get_width() - 280), 420), (260, 50), self.font,
                              enabled=True)
        continue_btn = Button("Continue", ((self.surface.get_width() - 260), 360), (240, 50), self.font,
                              enabled=True)
        typer_render = TextRenderer(self.font, color=(255, 255, 255))
        land_image = pygame.image.load("Assets/Sprites/Screens/landing.png")
        game_logo = land_image.get_rect(center=(120, (self.surface.get_height() // 2) - 150))
        game_logo_sized = pygame.transform.scale(land_image, (256, 256))

        running_menu = True
        while running_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_btn.is_clicked(event.pos):
                        return self.run_menu()
                    if new_btn.is_clicked(event.pos):
                        return self.new_game_menu()
                    if loadgame_btn.is_clicked(event.pos):
                        print("Loading game...")
                    if continue_btn.is_clicked(event.pos):
                        conn = sqlite3.connect("GameData/players.db")
                        cursor = conn.cursor()
                        cursor.execute("SELECT * FROM player ORDER BY id DESC LIMIT 1")
                        last_save = cursor.fetchone()
                        return "game"  # Switch to the game state

            self.surface.fill(self.bgc)  # Clear the surface for the campaign menu
            new_btn.draw(self.surface)
            back_btn.draw(self.surface)
            loadgame_btn.draw(self.surface)
            continue_btn.draw(self.surface)
            self.surface.blit(game_logo_sized, game_logo)
            typer_render.draw_text(self.surface, "Campaign Mode", (20, 20), 2000)
            pygame.display.flip()

        return "menu"