import pygame



class Button:
    def __init__(self, text, position, size, font, color=(100, 100, 100), text_color=(255, 255, 255), enabled=True):
        self.text = text
        self.position = position
        self.size = size
        self.font = font
        self.color = color
        self.text_color = text_color
        self.rect = pygame.Rect(position, size)
        self.enabled = enabled
        self.text_renderer = TextRenderer(font, text_color)

    def draw(self, surface):
        # Draw the button rectangle
        if not self.enabled:
            # Change color when disabled (e.g., gray out)
            disabled_color = (150, 150, 150)  # Example disabled color
            pygame.draw.rect(surface, disabled_color, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)

        # Render the text
        text_surfaces = self.text_renderer.render_text(self.text, self.rect.width)
        y_offset = (self.rect.height - sum(text_surface.get_height() for text_surface in text_surfaces)) // 2

        # Draw each line of text
        for text_surface in text_surfaces:
            text_rect = text_surface.get_rect()
            text_rect.centerx = self.rect.centerx
            text_rect.y = self.rect.y + y_offset
            surface.blit(text_surface, text_rect)
            y_offset += text_surface.get_height()

    def is_clicked(self, mouse_pos):
        # Only allow clicks if the button is not disabled
        if self.enabled:
            return self.rect.collidepoint(mouse_pos)
        return False

    def set_enabled(self, enabled):
        self.enabled = enabled  # Method to enable/disable the button

    def update_text(self, new_text):
        self.text = new_text


class TextRenderer:
    def __init__(self, font, color=(255, 255, 255)):
        if not isinstance(font, pygame.font.Font):
            raise ValueError("font must be a pygame.font.Font object")
        self.font = font
        self.color = color

    def render_text(self, text, max_width):
        words = text.split(' ')
        lines = []
        current_line = []

        for word in words:
            current_line.append(word)
            # Check the width of the current line
            line_surface = self.font.render(' '.join(current_line), True, self.color)
            if line_surface.get_width() > max_width:
                # If the line is too wide, remove the last word and start a new line
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]

        # Add the last line
        lines.append(' '.join(current_line))

        # Render each line
        text_surfaces = [self.font.render(line, True, self.color) for line in lines]
        return text_surfaces

    def draw_text(self, surface, text, position, max_width):
        text_surfaces = self.render_text(text, max_width)
        x, y = position

        for line_surface in text_surfaces:
            surface.blit(line_surface, (x, y))
            y += line_surface.get_height()
class InputBox:
    def __init__(self, position, size, font):
        self.position = position
        self.color = (0,0,0)
        self.size = size
        self.rect = pygame.Rect(self.position, self.size)
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
class ImageButton:
    def __init__(self, image_normal, image_hovered, image_focused, position, size):
        self.image_normal = image_normal
        self.image_hovered = image_hovered
        self.image_focused = image_focused
        self.position = position
        self.size = size
        self.rect = pygame.Rect(self.position, self.size)
        self.is_hovered = False
        self.is_focused = False
        self.mask_normal = pygame.mask.from_surface(self.image_normal)
        self.mask_hovered = pygame.mask.from_surface(self.image_hovered)
        self.mask_focused = pygame.mask.from_surface(self.image_focused)

    def draw(self, surface):
        if self.is_hovered:
            surface.blit(self.image_hovered, self.rect)
        else:
            if self.is_focused:
                surface.blit(self.image_focused, self.rect)
            else:  # Default to normal image
                surface.blit(self.image_normal, self.rect)

    def is_clicked(self, pos):
        # Check if the click is within the button's rectangle
        if not self.rect.collidepoint(pos):
            return False

        # Calculate the position relative to the button's top-left corner
        relative_x = pos[0] - self.rect.x
        relative_y = pos[1] - self.rect.y

        # Use the appropriate mask based on the current state
        if self.is_hovered:
            return self.mask_hovered.get_at((relative_x, relative_y))
        elif self.is_focused:
            return self.mask_focused.get_at((relative_x, relative_y))
        else:
            return self.mask_normal.get_at((relative_x, relative_y))

    def update(self, mouse_pos):
        # Check if the mouse is within the button's rectangle
        if not self.rect.collidepoint(mouse_pos):
            self.is_hovered = False
            return

        # Calculate the position relative to the button's top-left corner
        relative_x = mouse_pos[0] - self.rect.x
        relative_y = mouse_pos[1] - self.rect.y

        # Use the appropriate mask to determine hover state
        if self.mask_normal.get_at((relative_x, relative_y)):
            self.is_hovered = True
        else:
            self.is_hovered = False

    def in_focus(self, state=False):
        self.is_focused = state
