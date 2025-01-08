import pygame
from UIElements import TextRenderer, Button, InputBox
import os
import sqlite3

class Menu:
    def __init__(self, surface, screen):
        pygame.init()
        pygame.mixer.init()
        self.screen = screen
        self.surface = surface
        self.font_path = os.path.join("HomeVideo-Regular", "Assets/fonts/Game/HomeVideo-Regular.otf")
        self.font = pygame.font.Font('Assets/fonts/Game/HomeVideo-Regular.otf', 48)
        self.button_font = TextRenderer(self.font, color=(255, 255, 255))
        self.music = pygame.mixer.Sound("Assets/Sound/Music/dreadful_horizon.wav")
        self.music.set_volume(0.4)
        self.music.play(-1)

        self.gameIcon = pygame.image.load("Assets/Sprites/icons/Icon33.png")
        pygame.display.set_caption("Raiders of Elysium")

        self.bgc = pygame.image.load("Assets/Sprites/Backdrops/NormalBackground.png")
        pygame.display.set_icon(self.gameIcon)

    def stop_music(self):
        self.music.stop()

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
                    self.stop_music()
                    self.screen.search_new_state("quit")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if quit_button.is_clicked(event.pos):
                        self.stop_music()
                        self.screen.search_new_state("quit")
                    if instant_action_button.is_clicked(event.pos):
                        self.stop_music()
                        self.screen.search_new_state("game")
                    if campaign_button.is_clicked(event.pos):
                        return self.Run_CampaignMenu()

            self.surface.blit(self.bgc, (0,0))

            name_render = TextRenderer(self.font, color=(255, 255, 255))
            name_render.draw_text(self.surface, "RAIDERS OF ELYSIUM", (20, 20), 2000)

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
                    self.stop_music()
                    self.screen.search_new_state("quit")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if create_button.is_clicked(event.pos):
                        self.new_gameSQL(name_ib.get_name())
                        self.stop_music()
                        self.screen.search_new_state("shell")
                    elif back_btn.is_clicked(event.pos):
                        return self.Run_CampaignMenu()
                name_ib.handle_event(event)
            self.surface.blit(self.bgc,(0,0))
            create_button.draw(self.surface)
            back_btn.draw(self.surface)
            name_ib.draw(self.surface)
            pygame.display.flip()

        return "menu"

    def new_gameSQL(self, profile_name=None):
        connection = sqlite3.connect("GameData/players.db")
        self.cursor = connection.cursor()
        if profile_name is not None:
            profile_dir = "GameData/Profiles/" + profile_name + ".db"
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
                        storage TEXT NOT NULL,
                        gear TEXT NOT NULL
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
                    self.stop_music()
                    self.screen.search_new_state("quit")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_btn.is_clicked(event.pos):
                        return self.run_menu()
                    if new_btn.is_clicked(event.pos):
                        return self.new_game_menu()
                    if loadgame_btn.is_clicked(event.pos):
                        print("Loading game...")
                        return self.load_game_menu()
                    if continue_btn.is_clicked(event.pos):
                        conn = sqlite3.connect("GameData/players.db")
                        cursor = conn.cursor()
                        cursor.execute("SELECT * FROM player ORDER BY id DESC LIMIT 1")
                        last_save = cursor.fetchone()
                        self.screen.save = last_save
                        print(last_save)
                        self.screen.search_new_state("shell")
                        return
            self.surface.blit(self.bgc,(0,0))  # Clear the surface for the campaign menu
            new_btn.draw(self.surface)
            back_btn.draw(self.surface)
            loadgame_btn.draw(self.surface)
            continue_btn.draw(self.surface)
            self.surface.blit(game_logo_sized, game_logo)
            typer_render.draw_text(self.surface, "Campaign Mode", (20, 20), 2000)
            pygame.display.flip()

        return "menu"

    def load_game_menu(self):
        back_btn = Button("Back", ((self.surface.get_width() - 220), 540), (200, 50), self.font, enabled=True)
        typer_render = TextRenderer(self.font, color=(255, 255, 255))

        # Connect to the database and retrieve the list of saved games
        conn = sqlite3.connect("GameData/players.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM player")
        saves = cursor.fetchall()
        conn.close()

        # Create buttons for each save
        load_buttons = []
        delete_buttons = []
        save_names = []
        y_offset = 100
        for save in saves:
            save_id, profile_dir, profile_name = save
            save_name = TextRenderer(self.font, color=(255, 255, 255), text=profile_name)
            load_btn = Button("Load", ((self.surface.get_width() - 400), y_offset), (180, 50), self.font, enabled=True)
            delete_btn = Button("Delete", ((self.surface.get_width() - 200), y_offset), (180, 50), self.font,
                                enabled=True)
            save_names.append(save_name)
            load_buttons.append((load_btn, save_id, profile_dir))  # Include save_id here
            delete_buttons.append((delete_btn, profile_dir))
            y_offset += 60

        running_menu = True
        while running_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop_music()
                    self.screen.search_new_state("quit")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_btn.is_clicked(event.pos):
                        return self.Run_CampaignMenu()
                    for load_btn, save_id, profile_dir in load_buttons:
                        if load_btn.is_clicked(event.pos):
                            self.load_game(save_id, profile_dir)
                            self.stop_music()
                            self.screen.search_new_state("shell")
                    for delete_btn, profile_dir in delete_buttons:
                        if delete_btn.is_clicked(event.pos):
                            self.delete_game(profile_dir)
                            return self.load_game_menu()

            self.surface.blit(self.bgc, (0, 0))
            typer_render.draw_text(self.surface, "Load Game", (20, 20), 2000)
            back_btn.draw(self.surface)
            y_offset = 100
            for save_name in save_names:
                save_name.draw_text(self.surface, None, ((self.surface.get_width() - 800), y_offset), 400)
                y_offset += 60
            for load_btn, _, _ in load_buttons:
                load_btn.draw(self.surface)
            for delete_btn, _ in delete_buttons:
                delete_btn.draw(self.surface)
            pygame.display.flip()

        return "menu"

    def load_game(self, save_id, profile_dir):
        print(f"Loading game with ID {save_id} from {profile_dir}")
        self.screen.save = (save_id, profile_dir)

    def delete_game(self, profile_dir):
        # Implement the logic to delete the game from the specified profile_dir
        print(f"Deleting game from {profile_dir}")
        conn = sqlite3.connect("GameData/players.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM player WHERE profile_dir = ?", (profile_dir,))
        conn.commit()
        conn.close()
        os.remove(profile_dir)
