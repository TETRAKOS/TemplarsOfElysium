import pygame



class Button:
    def __init__(self, text, position, size, font, color=(100, 100, 100), text_color=(255, 255, 255)):
        self.text = text
        self.position = position
        self.size = size
        self.font = font
        self.color = color
        self.text_color = text_color
        self.rect = pygame.Rect(position, size)

    def draw(self, surface):
        # Draw the button rectangle
        pygame.draw.rect(surface, self.color, self.rect)

        # Render the text
        text_surface, text_rect = self.font.render_text(self.text)
        text_rect.center = self.rect.center  # Center the text on the button
        surface.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


class TextRenderer:
    def __init__(self, font, color=(255, 255, 255)):
        self.font = font  # Accept a pygame.font.Font object
        self.color = color

    def render_text(self, text):
        text_surface = self.font.render(text, False, self.color)  # Use True for anti-aliasing
        text_rect = text_surface.get_rect()
        return text_surface, text_rect

    def draw_text(self, surface, text, position):
        text_surface, text_rect = self.render_text(text)
        text_rect.topleft = position
        surface.blit(text_surface, text_rect)



