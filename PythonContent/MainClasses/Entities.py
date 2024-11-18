import pygame


class Actor:
    def __init__(self, pos, icon):
        self.pos = pos
        self.icon = pygame.image.load(icon)
        self.rect = pygame.Rect(pos, self.icon.get_size())
class Wall(Actor):
    def __init__(self, pos):
        super().__init__(pos, "Assets/Sprites/Entities/MapAssets/Wall/Wall_default.png")
    #def __str__(self):
     #   print("Wall")
class Player(Actor):
    def __init__(self, pos, icon):
        super().__init__(pos, icon)
        self.inventory = []
        self.icon = pygame.image.load("Assets/Sprites/Entities/Creatures/Player/fig1.png")
        self.rect = pygame.Rect(pos, self.icon.get_size())
        self.resource = 0
    def handle_input(self, event):
        move = (0,0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move = (0, -1)
            elif event.key == pygame.K_DOWN:
                move = (0, 1)
            elif event.key == pygame.K_LEFT:
                move = (-1, 0)
            elif event.key == pygame.K_RIGHT:
                move = (1, 0)
        return move
class Hostile(Actor):
    def __init__(self, pos, icon):
        super().__init__(pos, icon)
        self.icon = pygame.image.load("Assets/Sprites/Entities/Creatures/Walker/walker.png")
        self.rect = pygame.Rect(pos, self.icon.get_size())
class Walker(Hostile):
    def __init__(self, pos):
        super().__init__(pos, "Assets/Sprites/Entities/Creatures/Walker/walker.png")
