import pygame
import random
import Entities
import json
import os
from Mission_manager import Mission

def sorting_key(value):
    if isinstance(value, Entities.Player):
        return 0
    elif isinstance(value, Entities.Hostile):
        return 1
    elif isinstance(value, Entities.Actor):
        return 2
    elif isinstance(value, Entities.Wall):
        return 3
    elif isinstance(value, str):
        return 4
    else:
        return 5

class Grid:
    def __init__(self, width, height, cell_size, game):
        self.game = game
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid = [[[] for _ in range(width)] for _ in range(height)]
        self.rooms = []
        self.images = {}
        self.mission = Mission(self.game, self, "scout")
        self.asset_paths = self.load_asset_paths()
        self.load_images()

    def load_asset_paths(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        asset_path_file = os.path.join(script_dir, 'Assets', 'dicts', 'asset_paths.js')
        with open(asset_path_file, 'r') as f:
            return json.load(f)

    def load_room_layouts(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        asset_path_file = os.path.join(script_dir, 'Assets', 'dicts', 'rooms_layout.js')
        with open(asset_path_file, 'r') as f:
            return json.load(f)

    def load_room_content(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        asset_path_file = os.path.join(script_dir, 'Assets', 'dicts', 'rooms_content.js')
        with open(asset_path_file, 'r') as f:
            return json.load(f)

    def load_images(self):
        for key, path in self.asset_paths.items():
            self.images[key] = pygame.image.load(path)

    def generate_dungeon(self):
        self.rooms = []
        room_layouts = self.load_room_layouts()
        room_content = self.load_room_content()
        name, basic, danger, loot, end = self.mission.generate_mission()
        layout_counts = {layout["layout"]: 0 for layout in room_layouts}
        attempts = 0
        max_attempts = (basic + danger + loot) * 3  # Limit attempts to avoid infinite loops

        # Find the elevator layout
        elevator_layout = next(layout for layout in room_layouts if layout["layout"] == "elevator")

        # Generate the first (elevator) room
        room_width = elevator_layout["x"]
        room_height = elevator_layout["y"]
        x = random.randint(1, self.width - room_width - 2)
        y = random.randint(1, self.height - room_height - 2)
        first_room = (x, y, room_width, room_height, elevator_layout["layout"], elevator_layout["loot_value"],
                      elevator_layout["danger"], elevator_layout["tile"])

        self.add_room(first_room)
        self.enrich_room(first_room, room_content)
        self.rooms.append(first_room)
        layout_counts[elevator_layout["layout"]] += 1

        # Generate middle rooms
        while len(self.rooms) < (basic + danger + loot - 1) and attempts < max_attempts:
            layout = random.choice([l for l in room_layouts if l["layout"] != "elevator"])
            if layout_counts[layout["layout"]] >= layout["max_count"]:
                attempts += 1
                continue

            room_width = layout["x"]
            room_height = layout["y"]
            x = random.randint(1, self.width - room_width - 2)
            y = random.randint(1, self.height - room_height - 2)
            new_room = (
                x, y, room_width, room_height, layout["layout"], layout["loot_value"], layout["danger"], layout["tile"])

            if not any(self.overlap(new_room, r) for r in self.rooms):
                self.add_room(new_room)
                self.enrich_room(new_room, room_content)
                self.rooms.append(new_room)
                layout_counts[layout["layout"]] += 1

            attempts += 1

        # Generate the last (elevator) room
        x = random.randint(1, self.width - room_width - 2)
        y = random.randint(1, self.height - room_height - 2)
        last_room = (x, y, room_width, room_height, elevator_layout["layout"], elevator_layout["loot_value"],
                     elevator_layout["danger"], elevator_layout["tile"])

        while self.overlap(last_room, self.rooms[-1]):
            x = random.randint(1, self.width - room_width - 2)
            y = random.randint(1, self.height - room_height - 2)
            last_room = (x, y, room_width, room_height, elevator_layout["layout"], elevator_layout["loot_value"],
                         elevator_layout["danger"], elevator_layout["tile"])

        self.add_room(last_room)
        self.enrich_room(last_room, room_content)
        self.rooms.append(last_room)
        layout_counts[elevator_layout["layout"]] += 1

        # Connect rooms
        for i in range(1, len(self.rooms)):
            self.connect_rooms(self.rooms[i - 1], self.rooms[i])

        self.encase_rooms()

        print(f"Generated {len(self.rooms)} rooms")
        for layout, count in layout_counts.items():
            print(f"{layout}: {count}")

        # Generate loot
    def generate_loot(self):
        for room in self.rooms:
            if room[5] > 0:  # Check if the room has a non-zero loot value
                x, y, _, _, _, loot_value, _, _ = room
                num_loots = random.randint(1, loot_value)  # Adjust the range as needed
                for _ in range(num_loots):
                    loot_pos_x = random.randint(x + 1, x + room[2] - 2)  # Avoid placing on walls
                    loot_pos_y = random.randint(y + 1, y + room[3] - 2)  # Avoid placing on walls
                    self.set_cell(loot_pos_x, loot_pos_y, Entities.Loot(self.game, [loot_pos_x, loot_pos_y],
                                                                        "Assets\Sprites\Entities\MapAssets\Loot\Bag\Bag_o.png"))

    def get_starting_point(self):
        room = self.rooms[0]
        x = (room[0])
        y = (room[1])
        print(x, y)
        return [x, y]

    def add_random_items(self):
        items = ["d", "g"]  # "d" for dust, "g" for garbage
        for room in self.rooms:
            x, y, width, height, layout, loot_value, danger, tile = room
            num_items = random.randint(5, 15)  # Adjust the range as needed
            for _ in range(num_items):
                item = random.choice(items)
                attempts = 0
                while attempts < 10:  # Limit attempts to avoid infinite loop
                    item_x = random.randint(x + 1, x + width - 2)  # Avoid placing on walls
                    item_y = random.randint(y + 1, y + height - 2)  # Avoid placing on walls
                    if self.cell_contains(item_x, item_y, tile) and not self.cell_contains(item_x, item_y, item):
                        self.set_cell(item_x, item_y, item)
                        print(f"Item {item} added at ({item_x}, {item_y})")
                        break
                    attempts += 1

    def find_closest_room(self, room):
        x1, y1, _, _ = room
        center1 = (x1 + (room[2] // 2), y1 + (room[3] // 2))

        closest_room = None
        closest_distance = float('inf')

        for existing_room in self.rooms:
            if existing_room == room:
                continue

            x2, y2, _, _ = existing_room
            center2 = (x2 + (existing_room[2] // 2), y2 + (existing_room[3] // 2))  # Center of the existing room

            distance = ((center1[0] - center2[0]) ** 2 + (center1[1] - center2[1]) ** 2) ** 0.5

            if distance < closest_distance:
                closest_distance = distance
                closest_room = existing_room

        return closest_room

    def overlap(self, new_room, existing_room):
        x1, y1, w1, h1 = new_room[:4]
        x2, y2, w2, h2 = existing_room[:4]
        return not (x1 + w1 <= x2 or x2 + w2 <= x1 or y1 + h1 <= y2 or y2 + h2 <= y1)

    def add_room(self, room):
        x, y, width, height, layout, loot_value, danger, tile = room
        for i in range(y, y + height):
            for j in range(x, x + width):
                self.set_cell(j, i, tile)  # Set floor tile

    def enrich_room(self, room, room_content):
        x, y, width, height, layout, loot_value, danger, tile = room
        items = ["d", "g", "s", "r"]  # "d" for dust, "g" for garbage
        for i in range(danger):
            xr = x + random.randint(1, width - 2)
            yr = y + random.randint(1, height - 2)
            enemy_to_add = Entities.Hostile(self.game, [xr, yr], "Assets/Sprites/Entities/Creatures/Walker/walker.png")
            self.set_cell(xr, yr, enemy_to_add)
            self.game.enemies.append(enemy_to_add)

        # Add room-specific content
        for content in room_content:
            if content["layout"] == layout:
                for item in content["content"]:
                    pos_x, pos_y = item["position"]
                    texture_path = item["texture"]
                    item_x = x + pos_x
                    item_y = y + pos_y
                    self.set_cell(item_x, item_y, Entities.Actor(pos=[item_x, item_y], icon=texture_path))

        num_items = random.randint(1, 20)  # Adjust the range as needed
        for _ in range(num_items):
            item = random.choice(items)
            item_x = random.randint(x + 1, x + width - 2)  # Avoid placing on walls
            item_y = random.randint(y + 1, y + height - 2)  #^
            self.set_cell(item_x, item_y, item)
             #   break
        # for s in range(loot_value):
        #     xr = x + random.randint(1, width - 2)
        #     yr = y + random.randint(1, height - 2)
        #     self.set_cell(xr,yr,Entities.Loot(self.game,[xr,yr],"Assets\Sprites\Entities\MapAssets\Loot\Bag\Bag_o.png"))

    def encase_rooms(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.cell_contains(x, y, '.'):
                    if x - 1 >= 0 and self.cell_contains(x - 1, y, ".") is None and self.cell_contains(x - 1, y, Entities.Actor) is None:  # Left
                        self.set_cell(x - 1, y, self.get_wall_sprite((x - 1, y)))
                    if x + 1 < self.width and self.cell_contains(x + 1, y, ".") is None and self.cell_contains(x - 1, y, Entities.Actor) is None:  # Right
                        self.set_cell(x + 1, y, self.get_wall_sprite((x + 1, y)))
                    if y - 1 >= 0 and self.cell_contains(x, y - 1, ".") is None and self.cell_contains(x - 1, y, Entities.Actor) is None:  # Top
                        self.set_cell(x, y - 1, self.get_wall_sprite((x, y - 1)))
                    if y + 1 < self.height and self.cell_contains(x, y + 1, ".") is None and self.cell_contains(x - 1, y, Entities.Actor) is None:  # Bottom
                        self.set_cell(x, y + 1, self.get_wall_sprite((x, y + 1)))

    def connect_rooms(self, room1, room2):
        x1, y1, w1, h1 = room1[:4]
        x2, y2, w2, h2 = room2[:4]

        # Calculate the centers of the rooms
        center1 = (x1 + w1 // 2, y1 + h1 // 2)
        center2 = (x2 + w2 // 2, y2 + h2 // 2)

        # Determine the closest points on the edges of the rooms
        if center1[0] < center2[0]:  # room1 is to the left of room2
            edge1_x = x1 + w1
            edge2_x = x2
        else:  # room1 is to the right of room2
            edge1_x = x1
            edge2_x = x2 + w2

        if center1[1] < center2[1]:  # room1 is above room2
            edge1_y = y1 + h1
            edge2_y = y2
        else:  # room1 is below room2
            edge1_y = y1
            edge2_y = y2 + h2

        # Find the closest points on the vertical and horizontal edges
        if abs(edge1_x - edge2_x) > abs(edge1_y - edge2_y):
            # Horizontal corridor is longer, so connect vertically first
            edge1 = (edge1_x, random.randint(y1, y1 + h1 - 1))
            edge2 = (edge2_x, random.randint(y2, y2 + h2 - 1))
            self.draw_horizontal_corridor(edge1[0], edge2[0], edge1[1])
            self.draw_vertical_corridor(edge1[1], edge2[1], edge2[0])
        else:
            # Vertical corridor is longer, so connect horizontally first
            edge1 = (random.randint(x1, x1 + w1 - 1), edge1_y)
            edge2 = (random.randint(x2, x2 + w2 - 1), edge2_y)
            self.draw_vertical_corridor(edge1[1], edge2[1], edge1[0])
            self.draw_horizontal_corridor(edge1[0], edge2[0], edge2[1])

        # Place a door at the starting point of the corridor
        door = Entities.Door((edge1[0], edge1[1]), "Assets/Sprites/Entities/MapAssets/Door/Door_closed.png")
        door2 = Entities.Door((edge2[0], edge2[1]), "Assets/Sprites/Entities/MapAssets/Door/Door_closed.png")
        self.set_cell(edge1[0], edge1[1], door)
        self.set_cell(edge2[0], edge2[1], door2)

    def draw_horizontal_corridor(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.set_cell(x, y, "bw")
            cell = self.grid[y][x]
            if "r" and "." in cell:
                self.remove_from_cell(x, y, "bw")

    def draw_vertical_corridor(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.set_cell(x, y, "bn")
            cell = self.grid[y][x]
            if "bn" and "." in cell:
                self.remove_from_cell(x, y, "bn")
        min_y, max_y = min(y1, y2), max(y1, y2)
        for y in [min_y, max_y]:
            cell_v = self.get_cell(x, y)
            if "bn" in cell_v:
                if (y == min_y and "." in self.get_cell(x, y - 1)) or \
                        (y == max_y and "." in self.get_cell(x, y + 1)):
                    self.remove_from_cell(x, y, "bn")

    def set_cell(self, x, y, value):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x].append(value)
            self.sort_cell(x, y)

    def remove_from_cell(self, x, y, actor):
        if 0 <= x < self.width and 0 <= y < self.height:
            if actor in self.grid[y][x]:  # Ensure the actor exists in the cell before removing it
                self.grid[y][x].remove(actor)

    def sort_cell(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x].sort(key=sorting_key)

    def get_cell(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return []

    def cell_contains(self, x, y, value):
        cell = self.get_cell(x, y)
        for item in cell:
            if isinstance(item, type(value)) or item == value:
                return item
        return None

    def draw(self, surface, camera, visibility_grid):
        floor_sprites = []
        decor_sprites = []
        actor_sprites = []

        for y in range(self.height):
            for x in range(self.width):
                if visibility_grid[y][x]:
                    rect = pygame.Rect(x * self.cell_size - camera[0], y * self.cell_size - camera[1], self.cell_size,
                                       self.cell_size)
                    cell_values = self.grid[y][x]
                    for value in cell_values:
                        if value in self.images:
                            if value == '.' or value == 'sci' or value == 'str':
                                floor_sprites.append((self.images[value], rect))
                            else:
                                decor_sprites.append((self.images[value], rect))
                        if isinstance(value, Entities.Actor):
                            actor_sprites.append((value.icon, rect))

        # Render floor sprites
        for image, rect in floor_sprites:
            surface.blit(image, rect)

        # Render decor sprites
        for image, rect in decor_sprites:
            surface.blit(image, rect)

        # Render actor sprites
        for image, rect in actor_sprites:
            surface.blit(image, rect)

    def get_actors(self):
        actors = []
        for y in range(self.height):
            for x in range(self.width):
                cell_values = self.grid[y][x]
                for value in cell_values:
                    if isinstance(value, Entities.Actor):
                        actors.append(value)
        return actors

    def get_wall_sprite(self, pos):
        x, y = pos
        neighbors = [
            self.get_cell(x - 1, y),  # Left
            self.get_cell(x + 1, y),  # Right
            self.get_cell(x, y - 1),  # Top
            self.get_cell(x, y + 1)  # Bottom
        ]

        # Check if neighbors are walls
        left_wall = any(isinstance(item, Entities.Wall) for item in neighbors[0])
        right_wall = any(isinstance(item, Entities.Wall) for item in neighbors[1])
        top_wall = any(isinstance(item, Entities.Wall) for item in neighbors[2])
        bottom_wall = any(isinstance(item, Entities.Wall) for item in neighbors[3])

        return Entities.Wall(pos, "Assets/Sprites/Entities/MapAssets/Wall/Wall_cnc.png")  # Default wall

    def generate_minimap(self):
        minimap_surface = pygame.Surface((self.width, self.height))
        minimap_surface.fill((0, 0, 0))  # Fill with black background

        for y in range(self.height):
            for x in range(self.width):
                cell = self.get_cell(x, y)
                color = (0, 0, 0)  # Default color (black for unexplored)

                if any(isinstance(item, Entities.Wall) for item in cell):
                    color = (100, 100, 100)
                elif 'elv' in cell:
                    color = (200, 200, 200)
                elif any(isinstance(item, Entities.Actor) for item in cell):
                    color = (0, 255, 0)

                minimap_surface.set_at((x, y), color)

        return minimap_surface
