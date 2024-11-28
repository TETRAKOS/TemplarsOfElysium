import pygame
import Items
import UIElements
#from Overworld_game import Grid
def get_distance_from_actors(actor1,actor2):
    distance_x = abs(actor1.pos[0] - actor2.pos[0])
    distance_y = abs(actor1.pos[1] - actor2.pos[1])
    actor_distance = max(distance_x, distance_y)
    return actor_distance
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
    def event_use(self, actor):
        print(f"used by{actor}")
        pass

class Wall(Actor):
    def __init__(self, pos):
        super().__init__(pos, "Assets/Sprites/Entities/MapAssets/Wall/Wall_cnc.png")
        self.name = "Concrete wall"

    #def __str__(self):
     #   print("Wall")
class Inventory_component:
    def __init__(self, actor_ref):
        self.actor_ref = actor_ref
        self.items = []

    def add_item(self, item):
        self.items.append(item)
        print(f"Added {item.name} to inventory")

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            print(f"Removed {item.name} from inventory")

    def equip_weapon(self, weapon):
        if isinstance(weapon, Items.Weapon):
            if isinstance(self.actor_ref, Player):
                self.actor_ref.equip_weapon(weapon)

    def use_item(self, item):
        if isinstance(item, Items.Item):
            item.use(self)

class Player(Actor):
    def __init__(self, game, pos, icon):
        super().__init__(pos, icon)
        self.game = game
        self.inventory = Inventory_component(self)
        self.icon = pygame.image.load("Assets/Sprites/Entities/Creatures/Player/fig_east.png")
        self.rect = pygame.Rect(pos, self.icon.get_size())
        self.resource = 0
        self.name = "You"
        self.weapon = None
        self.event = "search"


    def handle_input(self, event):
        move = (0, 0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                move = (0, -1)
            elif event.key == pygame.K_s:
                move = (0, 1)
            elif event.key == pygame.K_a:
                self.icon = pygame.image.load("Assets/Sprites/Entities/Creatures/Player/fig_west.png")
                move = (-1, 0)
            elif event.key == pygame.K_d:
                self.icon = pygame.image.load("Assets/Sprites/Entities/Creatures/Player/fig_east.png")
                move = (1, 0)
        return move

    def pass_turn(self):
        self.game.pass_turn()

    def equip_weapon(self, weapon):
        self.weapon = weapon
        print(f"Equipped {weapon.name}")

    def attack(self, actor):
        if isinstance(self.weapon, Items.Weapon):
            if self.weapon.range >= get_distance_from_actors(self, actor):
                self.weapon.attack(actor)
                print(f"You attack {actor.name}")

    def search(self):
        print("You search around")

    def use(self, actor):
        if isinstance(actor, Actor) and not isinstance(actor, Hostile):
            a_distance = get_distance_from_actors(self, actor)
            if a_distance > 1:
                self.observe(actor)
            else:
                self.interact(actor)

    def observe(self, actor):
        if isinstance(actor, Actor):
            print(f"you looked at {actor.name}, it's too far to reach")
        else:
            print("incorrect Actor Type")

    def interact(self, actor):
        if isinstance(actor, Actor):
            print(f"You using {actor.name}")
            actor.event_use(self)
        else:
            print("incorrect Actor Type")

    def render_inventory(self, game_surface):
        inv_backdrop = UIElements.Rectangle(((game_surface.get_width() - 200), 0), (200, game_surface.get_height()), (70, 70, 70))
        inv_backdrop.draw(game_surface)
        y_offset = 50
     #   print("inventory drawn")
        for item in self.inventory.items:
            item_text = UIElements.TextRenderer(self.game.font_small, (255, 255, 255))
            item_text.draw_text(game_surface, item.name, (game_surface.get_width() - 190, y_offset), 190)
            y_offset += 30


class Hostile(Actor):
    def __init__(self, pos, icon):
        super().__init__(pos, icon)
        self.icon = pygame.image.load("Assets/Sprites/Entities/Creatures/Walker/walker.png")
        self.rect = pygame.Rect(pos, self.icon.get_size())
        self.name = "hostile"
        self.event = "attack"
        self.health = 5
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            print(f"{self.name} is dead")
            #self.game.remove_entity(self)
class Walker(Hostile):
    def __init__(self, pos):
        super().__init__(pos, "Assets/Sprites/Entities/Creatures/Walker/walker.png")
        self.name = "Walker"
class Loot(Actor):
    def __init__(self, game, pos, icon):
        super().__init__(pos, icon)
        self.game = game
        self.items = [Items.Shard(), Items.surv_pistol(None)]  # Add items to the loot
        self.name = "Bag with goods"
        self.enabled = True

    def event_use(self,player):
        if self.enabled:
            for item in self.items:
                    self.game.player.inventory.add_item(item)
            self.enabled = False
            self.icon = pygame.image.load("Assets\Sprites\Entities\MapAssets\Loot\Bag\Bag_o.png")
            #self.items = []  # Clear the loot after picking up
        return "use"