import pygame
import Entities
from Entities import Player, Hostile, Actor, Loot
from UIElements import Rectangle, TextRenderer, Button
#import Shaders
import Items
import MapGen
import math
class Game:
    def __init__(self):
        pygame.init()
        self.font = pygame.font.Font('Assets/fonts/Game/HomeVideo-Regular.otf', 32)
        self.font_small = pygame.font.Font('Assets/fonts/Game/HomeVideo-Regular.otf', 16)
        self.font_ann = pygame.font.Font('Assets/fonts/Game/HomeVideo-Regular.otf', 12)
        self.gameIcon = pygame.image.load("Assets/Sprites/icons/Icon33.png")
        pygame.display.set_icon(self.gameIcon)
        self.highlight = None  # (x, y, (color), end_time)
        self.surface = pygame.display.set_mode((1024, 724))
        self.bgc = (20, 25, 27)
        self.bgcd = (15, 20, 18)
        self.camera = [0, 0]
        self.enemies = []
        self.clock = pygame.time.Clock()
        self.grid = MapGen.Grid(80, 80, 40, self)
        self.grid.generate_dungeon()
        self.player_pos = self.grid.get_starting_point()
        self.player = Player(self, self.player_pos, "Assets/Sprites/Entities/Creatures/Player/fig1.png")
        self.setup_grid()
        self.grid.set_cell(self.player_pos[0], self.player_pos[1], self.player)
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                cell = self.grid.get_cell(x, y)
                if isinstance(cell, Hostile):
                    cell.game = self  # Set the game reference for the enemy
                    self.enemies.append(cell)
        self.enemy = Hostile(self, (5 * self.grid.cell_size, 5 * self.grid.cell_size),
                             "Assets/Sprites/Entities/Creatures/Walker/walker.png")
        self.turn_count = 0
        self.is_player_turn = True
        self.visibility_grid = [[False for _ in range(self.grid.width)] for _ in range(self.grid.height)]
        self.vision_radius = 10  # Adjust this value to change the player's vision range
        self.popup = None  # Initialize popup as None
        self.hit_highlight = None  # Initialize hit highlight as None
        self.map_loop()
    def get_player_charater(self):
        return self.player
    def setup_grid(self):
        self.grid.set_cell(7, 7, Loot(self, (7, 7), "Assets/Sprites/Entities/MapAssets/Loot/Bag/Bag.png"))
        self.grid.set_cell(self.player_pos[0] + 2, self.player_pos[1] + 2,
                           Loot(self, (self.player_pos[0] + 2, self.player_pos[1] + 2),
                                "Assets/Sprites/Entities/MapAssets/Loot/Bag/Bag.png"))

    def highlight_tile(self, x, y, color, duration):
        self.highlight = (x, y, color, pygame.time.get_ticks() + duration)
    def map_loop(self):
        backdrop = Rectangle(((self.surface.get_width() - 200), 0), (200, self.surface.get_height()), (70, 70, 70))
        turn_text = TextRenderer(self.font_small, (255, 255, 255))
        ammo_text = TextRenderer(self.font_small, (255, 255, 255))
        weapon_name = TextRenderer(self.font_small, (255, 255, 255))
        reload_button = Button("Reload", (self.surface.get_width() - 175, 350), (75, 50), self.font_small)
        weapon_mode = Button("Weapon Mode", (self.surface.get_width() - 85, 350), (75, 50), self.font_small)
        inventory_btn = Button("Inventory", (self.surface.get_width() - 175, 650), (150, 50), self.font_small)
        running = True
        inventory_open = False
        self.player.inventory.add_item(Items.Shard())
        self.popup = None
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if self.is_player_turn:  # Only handle input if it's the player's turn
                    move = self.player.handle_input(event)
                    if move != (0, 0):
                        self.move_player(move)
                        self.is_player_turn = False
                        self.turn_count += 1
                        self.handle_enemy_turn()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if inventory_open:
                            self.player.handle_inventory_click(mouse_pos)
                            if self.popup:
                                action = self.popup.handle_click(mouse_pos)
                                if action == "use":
                                    if isinstance(self.popup.item, Items.Weapon):
                                        self.player.equip_weapon(self.popup.item)
                                    else:
                                        self.player.inventory.use_item(self.popup.item)
                                elif action == "discard":
                                    self.player.inventory.remove_item(self.popup.item)
                                self.popup = None
                        tile_x = (mouse_pos[0] + self.camera[0]) // self.grid.cell_size
                        tile_y = (mouse_pos[1] + self.camera[1]) // self.grid.cell_size
                        cell_values = self.grid.get_cell(tile_x, tile_y)
                        for actor in cell_values:
                            if isinstance(actor, Actor):
                                actor_event = actor.is_clicked(mouse_pos)
                                if actor_event == "attack":
                                    hit_pos = self.player.attack(actor)
                                    if hit_pos:
                                        self.highlight_tile(hit_pos[0], hit_pos[1], (255, 0, 0),
                                                            200)
                                elif actor_event == "search":
                                    self.player.search()
                                elif actor_event == "use":
                                    self.player.use(actor)
                        if reload_button.is_clicked(mouse_pos):
                            if isinstance(self.player.weapon, Items.RangedWeapon):
                                self.player.weapon.reload()
                        elif weapon_mode.is_clicked(mouse_pos):
                            print("Weapon Mode")
                        elif inventory_btn.is_clicked(mouse_pos):
                            inventory_open = not inventory_open
                            if inventory_open:
                                inventory_btn.text = "Close"
                            else:
                                inventory_btn.text = "Inventory"

            self.surface.fill(self.bgc)
            self.update_camera()
            self.update_visibility()  # Update visibility
            clock = pygame.time.Clock()
            fps = str(clock.tick(60))
            pygame.display.set_caption("Templars of Elysium - Map" + fps)
            self.grid.draw(self.surface, self.camera, self.visibility_grid)

            backdrop.draw(self.surface)
            mouse_pos = pygame.mouse.get_pos()

            tile_x = (mouse_pos[0] + self.camera[0]) // self.grid.cell_size
            tile_y = (mouse_pos[1] + self.camera[1]) // self.grid.cell_size

            cell_values = self.grid.get_cell(tile_x, tile_y)

            for actor in cell_values:
                        if isinstance(actor, Actor) and self.visibility_grid[tile_y][tile_x]:
                            info_text = actor.getinfo()
                            text_surface = self.font_ann.render(info_text, True, (255, 255, 255))
                            text_rect = text_surface.get_rect(topleft=(mouse_pos[0] + 10, mouse_pos[1] + 10))
                            self.surface.blit(text_surface, text_rect)
                            pygame.draw.line(self.surface, (255, 255, 255),
                                             (self.player_pos[0] * self.grid.cell_size - self.camera[
                                                 0] + self.grid.cell_size // 2,
                                              self.player_pos[1] * self.grid.cell_size - self.camera[
                                                  1] + self.grid.cell_size // 2),
                                             mouse_pos)
                            if isinstance(actor, Hostile) and isinstance(self.player.weapon, Items.Weapon):
                                distance_x = abs(self.player_pos[0] - tile_x)
                                distance_y = abs(self.player_pos[1] - tile_y)
                                c_info = max(distance_x, distance_y)
                                c_text = f"Distance: {c_info} cells"
                                c_data = "weapon range " + str(self.player.weapon.range) if isinstance(
                                    self.player.weapon, Items.RangedWeapon) else ""
                                hit_chance = self.player.calculate_hit_chance(actor)
                                hit_text = f"Hit Chance: {hit_chance}%"
                                c_surface = self.font_small.render(c_data, True, (255, 255, 255))
                                text_surface = self.font_small.render(c_text, True, (
                                100, 100, 100) if c_info > self.player.weapon.range else (255, 0, 0))
                                hit_surface = self.font_small.render(hit_text, True, (255, 255, 255))
                                text_rect = text_surface.get_rect(topleft=(mouse_pos[0] + 10, mouse_pos[1] + 30))
                                range_rect = text_surface.get_rect(topleft=(mouse_pos[0] + 10, mouse_pos[1] + 50))
                                hit_rect = hit_surface.get_rect(topleft=(mouse_pos[0] + 10, mouse_pos[1] + 70))
                                self.surface.blit(text_surface, text_rect)
                                self.surface.blit(c_surface, range_rect)
                                self.surface.blit(hit_surface, hit_rect)
            else:
                pass
#                pygame.mouse.set_cursor(pygame.cursors.arrow)

            turn_message = "Your Turn" if self.is_player_turn else "Enemy's Turn"
            turn_text.draw_text(self.surface, turn_message, ((self.surface.get_width() - 150), 50), 100)
            if isinstance(self.player.weapon, Items.Weapon):
                weapon_icon = pygame.image.load(self.player.weapon.icon)
                weapon_name.draw_text(self.surface, self.player.weapon.name, (self.surface.get_width() - 150, 250), 50)
                if isinstance(self.player.weapon, Items.RangedWeapon):
                    ammo_text.draw_text(self.surface, str(self.player.weapon.ammo),
                                        (self.surface.get_width() - 150, 300), 50)
                    reload_button.draw(self.surface)

            else:
                weapon_icon = pygame.image.load("Assets/Sprites/Items/Weapons/Empty.png")
                weapon_name.draw_text(self.surface, "No weapon", (self.surface.get_width() - 190, 275), 200)
            weapon_mode.draw(self.surface)

            self.surface.blit(weapon_icon, (self.surface.get_width() - 150, 200))
            if inventory_open:
                self.player.render_inventory(self.surface)
            inventory_btn.draw(self.surface)
            if self.popup:
                self.popup.draw()
            if self.hit_highlight:
                hit_x, hit_y = self.hit_highlight
                pygame.draw.rect(self.surface, (255, 0, 0),
                                 (hit_x * self.grid.cell_size - self.camera[0],
                                  hit_y * self.grid.cell_size - self.camera[1],
                                  self.grid.cell_size, self.grid.cell_size), 2)

            if self.highlight:
                x, y, color, end_time = self.highlight
                if pygame.time.get_ticks() < end_time:
                    pygame.draw.rect(self.surface, color,
                                     (x * self.grid.cell_size - self.camera[0],
                                      y * self.grid.cell_size - self.camera[1],
                                      self.grid.cell_size, self.grid.cell_size))
                else:
                    self.highlight = None
            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()


    def pass_turn(self):
        print("Turn passed")
        self.is_player_turn = not self.is_player_turn
        self.handle_enemy_turn()

    def handle_enemy_turn(self):
        print("Enemy's turn")
        for enemy in self.enemies:
            if enemy.alive:
                enemy.take_turn(self.player_pos)
        self.is_player_turn = True


    def update_camera(self):
        self.camera[0] = self.player_pos[0] * self.grid.cell_size - self.surface.get_width() // 2 + self.grid.cell_size // 2
        self.camera[1] = self.player_pos[1] * self.grid.cell_size - self.surface.get_height() // 2 + self.grid.cell_size // 2

    def move_player(self, move):
        new_x = self.player_pos[0] + move[0]
        new_y = self.player_pos[1] + move[1]
        cell_values = self.grid.get_cell(new_x, new_y)
        can_move = True
        for item in cell_values:
            if isinstance(item, Entities.Actor) and item.collision:
                can_move = False
                break
        if can_move:
            #self.grid.set_cell(self.player_pos[0], self.player_pos[1], None) deprecated method
            self.grid.remove_from_cell(self.player_pos[0], self.player_pos[1],self.player)
            self.player_pos = [new_x, new_y]
            self.grid.set_cell(new_x, new_y, self.player)
            self.player.rect.topleft = (new_x * self.grid.cell_size, new_y * self.grid.cell_size)
            self.player.pos = [new_x, new_y]
            print(self.player.pos, self.grid.get_cell(self.player_pos[0], self.player_pos[1]))

    def update_visibility(self):
        self.visibility_grid = [[False for _ in range(self.grid.width)] for _ in range(self.grid.height)]
        self.cast_rays()

    def cast_rays(self):
        player_x, player_y = self.player_pos
        for angle in range(0, 360, 1):  # raycast by 1 degrees \ head direction mb?
            self.cast_ray(player_x, player_y, math.radians(angle))

    def cast_ray(self, start_x, start_y, angle):
        dx = math.cos(angle)
        dy = math.sin(angle)

        for i in range(self.vision_radius):
            x = int(start_x + dx * i)
            y = int(start_y + dy * i)

            if not self.is_valid(x, y):
                break

            self.visibility_grid[y][x] = True

            if self.is_wall(x, y):
                break

    def is_valid(self, x, y):
        return 0 <= x < self.grid.width and 0 <= y < self.grid.height

    def is_wall(self, x, y):
        cell_values = self.grid.get_cell(x, y)
        return any(isinstance(item, Entities.Wall) for item in cell_values) or (any(isinstance(item, Entities.Door)  and  item.collision == True for item in cell_values ))

    def update_hostile_positions(self):
        self.hostile_positions = {tuple(enemy.pos): enemy for enemy in self.enemies if enemy.alive}
def flood_fill(grid, start_pos, visibility_grid): #deprecated
        def is_valid(x, y):
            return 0 <= x < grid.width and 0 <= y < grid.height

        def is_wall(x, y):
            cell_values = grid.get_cell(x, y)
            return any(isinstance(item, Entities.Wall) for item in cell_values)

        stack = [start_pos]
        while stack:
            x, y = stack.pop()
            if is_valid(x, y) and not visibility_grid[y][x]:
                visibility_grid[y][x] = True
                if not is_wall(x, y):
                    stack.append((x + 1, y))
                    stack.append((x - 1, y))
                    stack.append((x, y + 1))
                    stack.append((x, y - 1))

if __name__ == "__main__":
    Game()