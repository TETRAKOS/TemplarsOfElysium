import pygame
import Entities
from Entities import Player, Hostile, Actor, Loot
from UIElements import Rectangle, TextRenderer, Button
#import Shaders
import Items
import MapGen
class Game:
    def __init__(self):
        pygame.init()
        self.font = pygame.font.Font('Assets/fonts/Game/HomeVideo-Regular.otf', 32)
        self.font_small = pygame.font.Font('Assets/fonts/Game/HomeVideo-Regular.otf', 16)
        self.font_ann = pygame.font.Font('Assets/fonts/Game/HomeVideo-Regular.otf', 12)
        self.gameIcon = pygame.image.load("Assets/Sprites/icons/Icon33.png")
        pygame.display.set_icon(self.gameIcon)

        self.surface = pygame.display.set_mode((1024, 724))
        self.bgc = (20, 25, 27)
        self.bgcd = (15, 20, 18)
        self.camera = [0, 0]
        self.clock = pygame.time.Clock()
        self.grid = MapGen.Grid(80, 80, 40)
        self.grid.generate_dungeon()
        self.player_pos = self.grid.get_starting_point()
        self.setup_grid()
        self.player = Player(self, self.player_pos, "Assets/Sprites/Entities/Creatures/Player/fig1.png")

        self.grid.set_cell(self.player_pos[0], self.player_pos[1], self.player)
        self.enemies = []
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                cell = self.grid.get_cell(x, y)
                if isinstance(cell, Hostile):
                    cell.game = self  # Set the game reference for the enemy
                    self.enemies.append(cell)
        #print(self.enemies)
        self.enemy = Hostile(self, (5 * self.grid.cell_size, 5 * self.grid.cell_size),
                             "Assets/Sprites/Entities/Creatures/Walker/walker.png")
        # self.grid.set_cell(5, 5, Hostile((5, 5), "Assets/Sprites/Entities/Creatures/Walker/walker.png"))
        self.turn_count = 0
        self.is_player_turn = True
        self.visibility_grid = [[False for _ in range(self.grid.width)] for _ in range(self.grid.height)]
        self.popup = None  # Initialize popup as None
        self.map_loop()

    def setup_grid(self):
        self.grid.set_cell(7, 7, Loot(self, (7, 7), "Assets/Sprites/Entities/MapAssets/Loot/Bag/Bag.png"))
        self.grid.set_cell(self.player_pos[0] + 2, self.player_pos[1] + 2,
                           Loot(self, (self.player_pos[0] + 2, self.player_pos[1] + 2),
                                "Assets/Sprites/Entities/MapAssets/Loot/Bag/Bag.png"))

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
                                    self.player.attack(actor)
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
                    if isinstance(actor, Loot):
                        pygame.mouse.set_cursor(pygame.cursors.ball)
                    if isinstance(actor, Hostile) and isinstance(self.player.weapon, Items.Weapon):
                        distance_x = abs(self.player_pos[0] - tile_x)
                        distance_y = abs(self.player_pos[1] - tile_y)
                        c_info = max(distance_x, distance_y)
                        c_text = f"Distance: {c_info} cells"
                        c_data = "weapon range " + str(self.player.weapon.range) if isinstance(self.player.weapon,
                                                                                               Items.RangedWeapon) else ""
                        c_surface = self.font_small.render(c_data, True, (255, 255, 255))
                        text_surface = self.font_small.render(c_text, True, (
                        100, 100, 100) if c_info > self.player.weapon.range else (255, 0, 0))
                        text_rect = text_surface.get_rect(topleft=(mouse_pos[0] + 10, mouse_pos[1] + 30))
                        range_rect = text_surface.get_rect(topleft=(mouse_pos[0] + 10, mouse_pos[1] + 50))
                        self.surface.blit(text_surface, text_rect), self.surface.blit(c_surface, range_rect)
            else:
                pygame.mouse.set_cursor(pygame.cursors.arrow)

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
                enemy.take_turn((self.player_pos[0], self.player_pos[1]))
        self.is_player_turn = True


    def update_camera(self):
        self.camera[0] = self.player_pos[0] * self.grid.cell_size - self.surface.get_width() // 2 + self.grid.cell_size // 2
        self.camera[1] = self.player_pos[1] * self.grid.cell_size - self.surface.get_height() // 2 + self.grid.cell_size // 2

    def move_player(self, move):
        new_x = self.player_pos[0] + move[0]
        new_y = self.player_pos[1] + move[1]
        cell_values = self.grid.get_cell(new_x, new_y)
        if not any(isinstance(item, Actor) for item in cell_values):
            #self.grid.set_cell(self.player_pos[0], self.player_pos[1], None) deprecated method
            self.grid.remove_from_cell(self.player_pos[0], self.player_pos[1],self.player)
            self.player_pos = [new_x, new_y]
            self.grid.set_cell(new_x, new_y, self.player)
            self.player.rect.topleft = (new_x * self.grid.cell_size, new_y * self.grid.cell_size)
            self.player.pos = [new_x, new_y]
            print(self.player.pos, self.grid.get_cell(self.player_pos[0], self.player_pos[1]))

    # def flood_fill(self, start_x, start_y, grid, radius):
    #     queue = [(start_x, start_y, 0)]
    #     visible_tiles = set()
    #     visited = set()
    #
    #     while queue:
    #         x, y, distance = queue.pop(0)
    #         if (x, y) in visited or distance > radius:
    #             continue
    #         visited.add((x, y))
    #         visible_tiles.add((x, y))
    #
    #         for dx in [-1, 0, 1]:
    #             for dy in [-1, 0, 1]:
    #                 if dx == 0 and dy == 0:
    #                     continue
    #                 nx, ny = x + dx, y + dy
    #                 if 0 <= nx < grid.width and 0 <= ny < grid.height:
    #                     cell_contents = grid.get_cell(nx, ny)
    #                     wall = grid.cell_contains(nx, ny, Entities.Wall)
    #                     if wall:
    #                         visible_tiles.add((nx, ny))
    #                     elif not wall and (nx, ny) not in visited:
    #                         queue.append((nx, ny, distance + 1))
    #     return visible_tiles
    #
    def update_visibility(self):
        visibility_grid = [[False for _ in range(self.grid.width)] for _ in range(self.grid.height)]
        flood_fill(self.grid, self.player_pos, visibility_grid)

def flood_fill(grid, start_pos, visibility_grid):
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