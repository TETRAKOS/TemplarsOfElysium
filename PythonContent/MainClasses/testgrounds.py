from UIElements import TextRenderer
import pygame

def main():
    # Initialize Pygame
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Text Renderer Example")

    # Create an instance of TextRenderer
    text_renderer = TextRenderer(font_name='Arial', font_size=48, color=(255, 255, 255))

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Fill the screen with a color (optional)
        screen.fill((0, 0, 0))  # Black background

        # Draw text using the TextRenderer
        text_renderer.draw_text(screen, "Hello, Pygame!", (100, 100))

        # Update the display
        pygame.display.flip()


if __name__ == "__main__":
    main()