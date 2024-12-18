import pygame
import Items
import UIElements
import Utils


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
        self.collision = True
    def onhover(self,event_pos):
        return self.rect.collidepoint(event_pos)
    def getinfo(self):
        return self.name
    def is_clicked(self, mouse_pos):
        return self.event
    def event_use(self, actor):
        print(f"used by{actor}")
        pass

class Wall(Actor):
    def __init__(self, pos, sprite_path):
        super().__init__(pos, sprite_path)
        self.name = "Concrete wall"
class Door(Actor):
    def __init__(self, pos, icon):
        super().__init__(pos, icon)
        self.name = "Door"
        self.icon = pygame.image.load("Assets/Sprites/Entities/MapAssets/Door/Door_closed.png")
        self.event = "use"
        self.collision = True


    def event_use(self,actor):
        if self.collision:
            self.collision = False
            self.icon = pygame.image.load("Assets/Sprites/Entities/MapAssets/Door/Door_opened.png")
        else:
            self.collision = True
            self.icon = pygame.image.load("Assets/Sprites/Entities/MapAssets/Door/Door_closed.png")

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
        for item in self.inventory.items:
            item_text = UIElements.TextRenderer(self.game.font_small, (255, 255, 255))
            item_text.draw_text(game_surface, item.name, (game_surface.get_width() - 190, y_offset), 190)
            y_offset += 30


    def handle_inventory_click(self, mouse_pos):
        y_offset = 50
        for item in self.inventory.items:
            item_rect = pygame.Rect((self.game.surface.get_width() - 190, y_offset), (190, 30))
            if item_rect.collidepoint(mouse_pos):
                self.game.popup = InventoryPopup(item, (mouse_pos[0], mouse_pos[1]), self.game.surface)
                return
            y_offset += 30

    def calculate_hit_chance(self, target):
        if not isinstance(self.weapon, Items.RangedWeapon):
            return 0
        distance = max(abs(self.pos[0] - target.pos[0]), abs(self.pos[1] - target.pos[1]))
        base_chance = 100 - (distance * 5)
        return max(min(base_chance, 95), 5)

class InventoryPopup:
    def __init__(self, item, pos, surface):
        self.item = item
        self.pos = pos
        self.surface = surface
        self.font = pygame.font.Font('Assets/fonts/Game/HomeVideo-Regular.otf', 16)
        self.use_button = UIElements.Button("Use", (pos[0], pos[1]), (50, 50), self.font)
        self.discard_button = UIElements.Button("Discard", (pos[0] - 60, pos[1]), (75, 50), self.font)

    def draw(self):
        self.use_button.draw(self.surface)
        self.discard_button.draw(self.surface)

    def handle_click(self, mouse_pos):
        if self.use_button.is_clicked(mouse_pos):
            return "use"
        elif self.discard_button.is_clicked(mouse_pos):
            return "discard"
        return None


class Hostile(Actor):
    def __init__(self, game, pos, icon):
        super().__init__(pos, icon)
        self.game = game  # Store the game reference
        self.icon = pygame.image.load("Assets/Sprites/Entities/Creatures/Walker/walker.png")
        self.rect = pygame.Rect(pos, self.icon.get_size())
        self.name = "hostile"
        self.event = "attack"
        self.health = 5
        self.alive = True  # Add an alive attribute

    def is_spotted(self):
        return self.game.visibility_grid[self.pos[1]][self.pos[0]]

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            print(f"{self.name} is dead")
            self.death()

    def death(self):
        self.icon = pygame.image.load("Assets/Sprites/Entities/Creatures/Dead/dead.png")
        self.alive = False
        self.collision = False

    def take_turn(self, player_pos):
      #  print("Take turn")
        if self.alive and self.is_spotted():
            distance = max(abs(self.pos[0] - player_pos[0]), abs(self.pos[1] - player_pos[1]))
            if distance <= 1:
                self.attack(player_pos)

            else:
                path = self.find_path(player_pos)
                print("find_path")
                if path:
                    self.move_towards(path)
                    print("moving")
    def attack(self, player_pos):
        print(f"{self.name} attacks the player at {player_pos}")
        # Implement attack logic here

    def find_path(self, target_pos):
        return Utils.a_star_search(self.game.grid, tuple(self.pos), tuple(target_pos), self.game)

    def move_towards(self, path):
        if path:
            next_pos = path[0]
            if not self.is_tile_occupied(next_pos):
                self.game.grid.remove_from_cell(self.pos[0], self.pos[1], self)
                self.pos = list(next_pos)
                self.game.grid.set_cell(self.pos[0], self.pos[1], self)
                self.rect.topleft = (self.pos[0] * self.game.grid.cell_size, self.pos[1] * self.game.grid.cell_size)
                self.game.update_hostile_positions()
                print(f"{self.name} moved to {self.pos}")

    def is_tile_occupied(self, pos):
        for hostile in self.game.enemies:
            if hostile != self and hostile.pos == list(pos):
                return True
        return False


class Walker(Hostile):
    def __init__(self, pos):
        super().__init__(pos, "Assets/Sprites/Entities/Creatures/Walker/walker.png")
        self.name = "Walker"
class Loot(Actor):
    def __init__(self, game, pos, icon):
        super().__init__(pos, icon)
        self.game = game
        self.items = [Items.Shard(), Items.smg(game.get_player_charater()), Items.surv_pistol(game.get_player_charater())]  # loot
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