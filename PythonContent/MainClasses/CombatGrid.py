import pygame
import math
from collections import deque

# Constants
WIDTH, HEIGHT = 800, 600
RADIUS = 30  # Radius of the hexagons
BACKGROUND_COLOR = (40, 40, 40)  # Background color
HEX_COLOR = (0, 0, 0, 128)  # Hexagon color with transparency (RGBA)
OUTLINE_COLOR = (255, 255, 255)  # White outline
HOVER_COLOR = (255, 0, 0, 128)  # Hover color
PLAYER_COLOR = (255, 255, 255)  # Player color
HIGHLIGHT_COLOR = (0, 255, 0, 128)  # Highlight color for reachable hexagons

DIRECTIONS = [
    (-1, 0),  # Up
    (-1, 1),  # Up-right
    (0, 1),   # Right
    (1, 0),   # Down
    (1, -1),  # Down-left
    (0, -1)   # Left
]

class Hexagon:
    def __init__(self, row, col, radius):
        self.row = row
        self.col = col
        self.radius = radius
        self.color = HEX_COLOR
        self.data = {}  # Dictionary to store additional data

    def get_position(self):
        """Calculate the center position of the hexagon."""
        x = self.col * (1.5 * self.radius)
        y = self.row * (math.sqrt(3) * self.radius)
        if self.col % 2 == 1:
            y += (math.sqrt(3) / 2) * self.radius
        return (x, y)

    def draw(self, surface, hover=False):
        """Draw the hexagon on the given surface."""
        x, y = self.get_position()
        color = HOVER_COLOR if hover else self.color
        points = []
        for i in range(6):
            angle = math.pi / 3 * i  # 60 degrees in radians
            point_x = x + self.radius * math.cos(angle)
            point_y = y + self.radius * math.sin(angle)
            points.append((point_x, point_y))

        # Draw the transparent hexagon
        pygame.draw.polygon(surface, color, points)
        # Draw the outline
        pygame.draw.polygon(surface, OUTLINE_COLOR, points, 1)  # 1 is the width of the outline

def is_mouse_over_hexagon(mouse_pos, hexagon):
    """Check if the mouse is over the hexagon."""
    mouse_x, mouse_y = mouse_pos
    hex_x, hex_y = hexagon.get_position()

    # Calculate the distance from the mouse to the center of the hexagon
    dx = mouse_x - hex_x
    dy = mouse_y - hex_y

    # Check if the mouse is within the hexagon's bounding box
    if abs(dy) < (math.sqrt(3) * hexagon.radius / 2) and abs(dx) < (1.5 * hexagon.radius):
        # Calculate the distance to the center of the hexagon
        distance_to_center = math.sqrt(dx ** 2 + dy ** 2)
        # Check if the distance is less than the radius
        return distance_to_center < hexagon.radius
    return False

class Player:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def move(self, direction):
        """Move the player in the specified direction."""
        if direction == "up-left":
            self.row -= 1
            self.col -= 1 if self.col % 2 == 1 else 0
        elif direction == "up-right":
            self.row -= 1
            self.col += 1 if self.col % 2 == 0 else 0
        elif direction == "right":
            self.col += 1
            elif direction == "down-right":
            self.row += 1
            self.col += 1 if self.col % 2 == 0 else 0
        elif direction == "down-left":
            self.row += 1
            self.col -= 1 if self.col % 2 == 1 else 0
        elif direction == "left":
            self.col -= 1

    def get_position(self):
        """Get the player's current position."""
        return (self.row, self.col)

    def draw(self, surface, hexagons):
        """Draw the player on the hexagonal grid."""
        x, y = hexagons[self.row][self.col].get_position()
        pygame.draw.circle(surface, PLAYER_COLOR, (int(x), int(y)), RADIUS // 2)

