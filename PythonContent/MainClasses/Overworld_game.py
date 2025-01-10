import sqlite3
import pygame
import Entities
from Entities import Player, Hostile, Actor, Loot
from UIElements import Rectangle, TextRenderer, Button
import Items
import MapGen
import math
import json

class Game:
    def __init__(self, surface, screen):
        self.font = pygame.font.Font('Assets/fonts/Game/HomeVideo-Regular.otf', 32)
        self.font_small = pygame.font.Font('Assets/fonts/Game/HomeVideo-Regular.otf', 16)
        self.font_ann = pygame.font.Font('Assets/fonts/Game/HomeVideo-Regular.otf', 12)
        self.gameIcon = pygame.image.load("Assets/Sprites/icons/Icon33.png")
        pygame.display.set_icon(self.gameIcon)
        self.highlight = None  # (x, y, (color), end_time)
        self.screen = screen
        self.bgc = pygame.image.load("Assets/Sprites/Backdrops/NormalBackground.png")
        self.bgcd = (15, 20, 18)
        self.camera = [0, 0]
        self.surface = surface
        self.enemies = []
        self.clock = pygame.time.Clock()
        self.grid = MapGen.Grid(80, 80, 40, self)
        self.grid.generate_dungeon()
        self.player_pos = self.grid.get_starting_point()
        self.player = Player(self, self.player_pos, "Assets/Sprites/Entities/Creatures/Player/fig1.png")
        self.grid.generate_loot()
        self.grid.set_cell(self.player_pos[0], self.player_pos[1], self.player)
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                cell = self.grid.get_cell(x, y)
                if isinstance(cell, Hostile):
                    cell.game = self
                    self.enemies.append(cell)
        self.enemy = Hostile(self, (5 * self.grid.cell_size, 5 * self.grid.cell_size),
                             "Assets/Sprites/Entities/Creatures/Walker/walker.png")
        self.turn_count = 0
        self.is_player_turn = True
        self.visibility_grid = [[False for _ in range(self.grid.width)] for _ in range(self.grid.height)]
        self.vision_radius = 10
        self.popup = None
        self.hit_highlight = None
        self.load_gear()


    def get_player_charater(self):
        return self.player

    def highlight_tile(self, x, y, color, duration):
        self.highlight = (x, y, color, pygame.time.get_ticks() + duration)

    def map_loop(self):
        backdrop = Rectangle(((self.surface.get_width() - 200), 0), (200, self.surface.get_height()), (70, 70, 70))
        turn_text = TextRenderer(self.font_small, (255, 255, 255))
        ammo_icon = pygame.image.load("Assets/Sprites/icons/ammo.png")
        ammo_icon = pygame.transform.scale(ammo_icon, (32, 32))
        ammo_text = TextRenderer(self.font_small, (255, 255, 255))
        weapon_name = TextRenderer(self.font_small, (255, 255, 255))
        health_text = TextRenderer(self.font_small, (255,255,255))
        health_icon = pygame.image.load("Assets/Sprites/icons/Health.png")
        health_icon = pygame.transform.scale(health_icon, (32, 32))
        extract_btn = Button("Evacuation", (self.surface.get_width() - 160, 75), (125, 50), self.font_small, (255,255,0),(0,0,0),enabled =False)
        reload_button = Button("Reload", (self.surface.get_width() - 175, 350), (75, 50), self.font_small)
        inventory_btn = Button("Inventory", (self.surface.get_width() - 175, 650), (150, 50), self.font_small)
        minimap = self.grid.generate_minimap()
        minimap_size = 190  # size minimap
        minimap = pygame.transform.scale(minimap, (minimap_size, minimap_size))
        minimap_pos = (self.surface.get_width() - minimap_size - 5, 450)
        running = True
        inventory_open = False
        self.popup = None
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pass
                if self.is_player_turn:
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
                        if extract_btn.is_clicked(mouse_pos):
                            self.save_gear()
                            self.screen.search_new_state("shell")
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
                        elif inventory_btn.is_clicked(mouse_pos):
                            inventory_open = not inventory_open
                            if inventory_open:
                                inventory_btn.text = "Close"
                            else:
                                inventory_btn.text = "Inventory"

            self.surface.blit(self.bgc,(0,0))
            self.update_camera()
            self.update_visibility()
            clock = pygame.time.Clock()
            fps = str(clock.tick(60))
            pygame.display.set_caption("Raiders of Elysium - Map")
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

            turn_message = "Your Turn" if self.is_player_turn else "Enemy's Turn"
            turn_text.draw_text(self.surface, turn_message, ((self.surface.get_width() - 150), 50), 100)
            if isinstance(self.player.weapon, Items.Weapon):
                weapon_icon = pygame.image.load(self.player.weapon.icon)
                weapon_name.draw_text(self.surface, self.player.weapon.name, (self.surface.get_width() - 150, 250), 50)
                if isinstance(self.player.weapon, Items.RangedWeapon):
                    ammo_text.draw_text(self.surface, str(self.player.weapon.ammo),
                                        (self.surface.get_width() - 100, 320), 50)
                    reload_button.draw(self.surface)
                    self.surface.blit(ammo_icon, (self.surface.get_width() - 120,300))

            else:
                weapon_icon = pygame.image.load("Assets/Sprites/Items/Weapons/Empty.png")
                weapon_name.draw_text(self.surface, "No weapon", (self.surface.get_width() - 190, 225), 200)

            self.surface.blit(weapon_icon, (self.surface.get_width() - 150, 150))
            if self.player_pos == self.grid.extract_point:
                extract_btn.draw(self.surface)
                extract_btn.set_enabled(True)
            else:
                extract_btn.set_enabled(False)
            #health display
            self.surface.blit(health_icon, (self.surface.get_width() - 180,300))
            health_text.draw_text(self.surface,str(self.player.health.health),(self.surface.get_width() - 160,320),200)
            self.surface.blit(minimap, minimap_pos)

            player_minimap_x = int(self.player_pos[0] * minimap_size / self.grid.width)
            player_minimap_y = int(self.player_pos[1] * minimap_size / self.grid.height)
            pygame.draw.circle(self.surface, (0, 0, 255),
                               (minimap_pos[0] + player_minimap_x, minimap_pos[1] + player_minimap_y), 2)

            #inventory
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

        return "shell"

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

    def show_game_over(self):
        self.clear_gear()
        self.advance_day()

        game_over_font = pygame.font.Font('Assets/fonts/Game/HomeVideo-Regular.otf', 64)
        game_over_text = TextRenderer(game_over_font, (255, 0, 0))
        expl_text = TextRenderer(self.font, (255, 255, 255))
        dead_image = pygame.image.load("Assets/Sprites/Entities/Creatures/Player/fig_dead.png")
        dead_image = pygame.transform.scale(dead_image, (80, 80))

        exit_button = Button("Confirm", (self.surface.get_width() // 2 - 50, self.surface.get_height() // 2 + 120),
                             (150, 50), self.font)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if exit_button.is_clicked(mouse_pos):
                        self.screen.search_new_state("shell")

            self.surface.blit(self.bgc, (0, 0))
            exit_button.draw(self.surface)
            self.surface.blit(dead_image, (512 - 20, 400 - 20))
            game_over_text.draw_text(self.surface, "Mission Failure", (25, self.surface.get_height() // 2 - 150), 1000,
                                     align="center")
            expl_text.draw_text(self.surface, "Your raider has died and all items have been lost",
                                (self.surface.get_width() // 3, self.surface.get_height() // 2 - 75), 400,
                                align="center")
            pygame.display.flip()
            self.clock.tick(60)

        self.map_loop()

    def check_health(self):
        if self.player.health.health <= 0:
            self.show_game_over()
        elif self.player.health.health <= 35:
            self.bgc = pygame.image.load("Assets/Sprites/Backdrops/DeathBackground.png")
        else:
            self.bgc = pygame.image.load("Assets/Sprites/Backdrops/NormalBackground.png")

    def clear_gear(self):
        conn = sqlite3.connect(self.screen.save[1])
        cursor = conn.cursor()
        cursor.execute("UPDATE profile_data SET gear = '' WHERE day = (SELECT MAX(day) FROM profile_data)")
        conn.commit()
        conn.close()

    def save_gear(self):
        saved_inventory = self.player.inventory.serialize()
        conn = sqlite3.connect(self.screen.save[1])
        cursor = conn.cursor()
        cursor.execute("UPDATE profile_data SET gear = ? WHERE day = (SELECT MAX(day) FROM profile_data)", (json.dumps(saved_inventory),))
        conn.commit()
        conn.close()
        self.advance_day()


    def load_gear(self):
        conn = sqlite3.connect(self.screen.save[1])
        cursor = conn.cursor()
        cursor.execute("SELECT gear FROM profile_data WHERE day = (SELECT MAX(day) FROM profile_data)")
        result = cursor.fetchone()
        conn.close()

        if result and result[0]:
            items_dump = result[0].split(',')
            items_dump = [item.strip('"[] ') for item in items_dump]  # Remove any brackets and extra spaces
            self.player.inventory.items = self.player.inventory.deserialize(items_dump)

    def advance_day(self):
        conn = sqlite3.connect(self.screen.save[1])
        cursor = conn.cursor()
        cursor.execute("UPDATE profile_data SET day = day + 1 WHERE day = (SELECT MAX(day) FROM profile_data)")
        conn.commit()
        conn.close()