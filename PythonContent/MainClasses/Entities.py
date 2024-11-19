import pygame
#from Overworld_game import Grid

class Actor:
    def __init__(self, pos, icon):
        self.pos = pos
        self.icon = pygame.image.load(icon)
        self.rect = pygame.Rect(pos, self.icon.get_size())
        self.name = "Unknown"
    def onhover(self,event_pos):
        return self.rect.collidepoint(event_pos)
    def getinfo(self):
        return self.name

class Wall(Actor):
    def __init__(self, pos):
        super().__init__(pos, "Assets/Sprites/Entities/MapAssets/Wall/Wall_default.png")
        self.name = "Concrete wall"

    #def __str__(self):
     #   print("Wall")
class Player(Actor):
    def __init__(self, pos, icon):
        super().__init__(pos, icon)
        self.inventory = []
        self.icon = pygame.image.load("Assets/Sprites/Entities/Creatures/Player/fig1.png")
        self.rect = pygame.Rect(pos, self.icon.get_size())
        self.resource = 0
        self.name = "You"
    def handle_input(self, event):
        move = (0,0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                move = (0, -1)
            elif event.key == pygame.K_s:
                move = (0, 1)
            elif event.key == pygame.K_a:
                move = (-1, 0)
            elif event.key == pygame.K_d:
                move = (1, 0)
        return move
class Hostile(Actor):
    def __init__(self, pos, icon):
        super().__init__(pos, icon)
        self.icon = pygame.image.load("Assets/Sprites/Entities/Creatures/Walker/walker.png")
        self.rect = pygame.Rect(pos, self.icon.get_size())
        self.name = "hostile"
class Walker(Hostile):
    def __init__(self, pos):
        super().__init__(pos, "Assets/Sprites/Entities/Creatures/Walker/walker.png")
        self.name = "Walker"
class Loot(Actor):
    def __init__(self, pos, icon):
        super().__init__(pos, icon)
        self.items = []
        self.name = "Bag with goods"