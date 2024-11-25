import pygame


class Controller:
    def __init__(self, hexagons):
        self.hexagons = hexagons

    def get_clicked_hexagon(self, mouse_pos):
        """Return the hexagon that was clicked based on mouse position."""
        for row in self.hexagons:
            for hexagon in row:
               if s_mouse_over_hexagon(mouse_pos, hexagon):
                    return hexagon
        return None