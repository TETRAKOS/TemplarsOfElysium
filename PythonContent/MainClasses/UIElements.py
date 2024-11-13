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

class InputBox:
    def __init__(self, position, size, font):
        self.color = (0,0,0)
        self.rect = pygame.Rect(position, size)
        self.pos = position
        self.size = size
        self.text = ''
        self.active = False
        self.font = pygame.font.Font("Assets/fonts/Game/HomeVideo-Regular.otf", 32)
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = (0,0,0) if self.active else (125,125,125)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                print(self.text)
                self.text = ""
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
    def draw(self,screen):
        pygame.draw.rect(screen, self.color, self.rect,2)
        text_surface = self.font.render(self.text, False, (0,0,0))
        screen.blit(text_surface,(self.rect.x + 5, self.rect.y + 5))

    def get_name(self):
        return self.text
