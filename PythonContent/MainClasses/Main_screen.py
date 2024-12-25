import pygame
from Global import Shell
from Overworld_game import Game
from Main_menu import Menu

def main():
    pygame.init()

    # Set up the display
    surface = pygame.display.set_mode((1024, 724))
    pygame.display.set_caption("Templars of Elysium")

    # Load fonts and game icon
    font = pygame.font.Font('Assets/fonts/Game/HomeVideo-Regular.otf', 32)
    font_small = pygame.font.Font('Assets/fonts/Game/HomeVideo-Regular.otf', 16)
    gameIcon = pygame.image.load("Assets/Sprites/icons/Icon33.png")
    pygame.display.set_icon(gameIcon)

    # Create instances of the Shell and Game classes
    menu = Menu(surface)
    shell = Shell(surface, font, font_small, gameIcon)
    game = Game(surface)
    game.surface = surface  # Set the surface for the Game class

    # Game state
    current_state = "shell"

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if current_state == "shell":
                    running = False
                running = False
        if current_state == "menu":
            current_state = menu_screen()
        elif current_state == "shell":
            current_state = shell.mission_screen()
        elif current_state == "game":
            current_state = game.map_loop()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()