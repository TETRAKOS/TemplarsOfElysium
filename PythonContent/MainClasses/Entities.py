import pygame
#from Overworld_game import Grid

class Actor:
    def __init__(self, pos, icon):
        self.pos = pos
        self.icon = pygame.image.load(icon)
        self.rect = pygame.Rect(pos, self.icon.get_size())
        self.name = "Unknown"
        self.event = "use"
    def onhover(self,event_pos):
        return self.rect.collidepoint(event_pos)
    def getinfo(self):
        return self.name
    def is_clicked(self, mouse_pos):
        return self.event#self.rect.collidepoint(mouse_pos)

class Wall(Actor):
    def __init__(self, pos):
        super().__init__(pos, "Assets/Sprites/Entities/MapAssets/Wall/Wall_default.png")
        self.name = "Concrete wall"

    #def __str__(self):
     #   print("Wall")
class Player(Actor):
    def __init__(self,game, pos, icon):
        super().__init__(pos, icon)
        self.game = game
        self.inventory = []
        self.icon = pygame.image.load("Assets/Sprites/Entities/Creatures/Player/fig1.png")
        self.rect = pygame.Rect(pos, self.icon.get_size())
        self.resource = 0
        self.name = "You"
        self.weapon = None
        self.event = "search"
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
    def pass_turn(self):
        self.game.pass_turn()
    def equip_weapon(self, weapon):
        self.weapon = weapon
        print(f"Equipped {weapon.name}")
    def attack(self,actor):
        print(f"You attack {actor.name}")
    def search(self):
        print("You search around")
    def use(self,actor, actor_pos):
        if isinstance(actor, Actor) and not isinstance(actor, Hostile):
            distance_x = abs(self.pos[0] - actor_pos[0])
            distance_y = abs(self.pos[1] - actor_pos[1])
            actor_distance = max(distance_x, distance_y)
            print(self.pos[0],self.pos[1])
            if  actor_distance > 1:
                self.observe(actor)
            else:
                self.interact(actor)
        #print(f"You use {actor.name}")
    def observe(self, actor):
        if isinstance(actor, Actor):
            print(f"you looked at {actor.name}, it's too far to reach")
        else:
            print("incorrect Actor Type")
    def interact(self, actor):
        if isinstance(actor, Actor):
            print(f"You using {actor.name}")
        else:
            print("incorrect Actor Type")
class Hostile(Actor):
    def __init__(self, pos, icon):
        super().__init__(pos, icon)
        self.icon = pygame.image.load("Assets/Sprites/Entities/Creatures/Walker/walker.png")
        self.rect = pygame.Rect(pos, self.icon.get_size())
        self.name = "hostile"
        self.event = "attack"
class Walker(Hostile):
    def __init__(self, pos):
        super().__init__(pos, "Assets/Sprites/Entities/Creatures/Walker/walker.png")
        self.name = "Walker"
class Loot(Actor):
    def __init__(self, pos, icon):
        super().__init__(pos, icon)
        self.items = []
        self.name = "Bag with goods"
