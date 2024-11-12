import pygame
from UIElements import TextRenderer, Button
import subprocess
import sys

# Initialize Pygame
pygame.init()

# Create an instance of TextRenderer
name_render = TextRenderer(font_name="Arial", font_size=48, color=(255, 255, 255))
button_font = TextRenderer(font_name="Arial", font_size=36, color=(255, 255, 255))

# Load game icon
gameIcon = pygame.image.load("Assets/Sprites/icons/Icon33.png")
pygame.display.set_caption("Templars of Elysium")

# Set up display
surface = pygame.display.set_mode((640, 480))
bgc = (45, 48, 44)
pygame.display.set_icon(gameIcon)

# Create buttons
quit_button = Button("Quit", (220, 320), (200, 50), button_font)
instant_action_button = Button("Instant Action", (220, 250), (200, 50), button_font)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if quit_button.is_clicked(event.pos):
                running = False
            if instant_action_button.is_clicked(event.pos):
                subprocess.Popen([sys.executable, "CombatGrid.py"])

    surface.fill(bgc)

    # Draw the title
    name_render.draw_text(surface, "TEMPLARS OF ELYSIUM", (100, 100))

    # Draw the buttons
    quit_button.draw(surface)
    instant_action_button.draw(surface)

    pygame.display.flip()

pygame.quit()
