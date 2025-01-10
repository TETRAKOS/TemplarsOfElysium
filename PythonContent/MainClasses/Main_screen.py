import pygame
from Global import Shell
from Overworld_game import Game
from Main_menu import Menu
class MainScreen:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((1024, 724))
        pygame.display.set_caption("Raiders of Elysium")
        self.font = pygame.font.Font('Assets/fonts/Game/HomeVideo-Regular.otf', 32)
        self.font_small = pygame.font.Font('Assets/fonts/Game/HomeVideo-Regular.otf', 16)
        self.gameIcon = pygame.image.load("Assets/Sprites/icons/Icon33.png")
        pygame.display.set_icon(self.gameIcon)
        self.state = "menu"
        self.save = None
    def main_menu(self):
        game_screen = Menu(self.surface,self)
        game_screen.run_menu()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            print(self.state)
        pygame.quit()

    def shell_menu(self):
        game_screen = Shell(self.surface, self.font, self.font_small, self.gameIcon, self,self.save)
        game_screen.mission_screen()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        pygame.quit()
    def game_menu(self):
        game_screen = Game(self.surface,self)
        game_screen.map_loop()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.search_new_state("shell")
    def search_new_state(self, state):
        self.state = state
        print("search triggered")
        if self.state == "shell":
            self.shell_menu()
        elif self.state == "game":
            self.game_menu()
        elif self.state == "menu":
            self.main_menu()
        else:
            pygame.quit()
if __name__ == "__main__":
    miner_virus = MainScreen()
    miner_virus.search_new_state("menu")