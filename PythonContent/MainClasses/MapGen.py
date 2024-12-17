import pygame
import random
import Entities
import json

ROOM_COUNT = 32
ROOM_MIN_SIZE = 10
ROOM_MAX_SIZE = 20

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
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid = [[[] for _ in range(width)] for _ in range(height)]
        self.rooms = []

    def generate_dungeon(self):
        self.rooms = []

        room_layouts = [
            {"layout": "manufacturing", "x": 10, "y": 15, "loot_value": 3, "danger": 5},
            {"layout": "sci", "x": 12, "y": 18, "loot_value": 2, "danger": 3},
            {"layout": "lab", "x": 12, "y": 4, "loot_value": 4, "danger": 4},
            {"layout": "storage", "x": 12, "y": 5, "loot_value": 1, "danger": 2},
        ]

        for layout in room_layouts:
            room_width = layout["x"]
            room_height = layout["y"]
            x = random.randint(1, self.width - room_width - 2)
            y = random.randint(1, self.height - room_height - 2)
            new_room = (x, y, room_width, room_height, layout["layout"], layout["loot_value"], layout["danger"])
            if any(self.overlap(new_room, r) for r in self.rooms):
                continue
            self.add_room(new_room)
            self.rooms.append(new_room)

        for i in range(1, len(self.rooms)):
            self.connect_rooms(self.rooms[i-1], self.rooms[i])
        self.encase_rooms()
        self.add_random_items()

    def get_starting_point(self):
        room = self.rooms[0]
        x = (room[0])
        y = (room[1])
        print(x,y)
        return [x,y]

    def add_loot(self):
        pass

    def add_random_items(self):
        items = ["d", "g"] # "j" not included
        for room in self.rooms:
            x, y, width, height, layout, loot_value, danger = room
            num_items = random.randint(10, 30)
            for s in range(num_items):
                item = random.choice(items)
                item_x = random.randint(x, x + width - 1)
                item_y = random.randint(y, y + height - 1)
                if self.cell_contains(item_x, item_y, '.') and not self.cell_contains(item_x, item_y, item):
                    self.set_cell(item_x, item_y, item)

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
        x, y, width, height, layout, loot_value, danger = room
        for i in range(y, y + height):
            for j in range(x, x + width):
                self.set_cell(j, i, '.')  # Set floor tile

    def encase_rooms(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.cell_contains(x, y,'.'):
                    if x - 1 >= 0 and self.cell_contains(x - 1, y,".") is None and self.cell_contains(x - 1, y,Entities.Actor) is None:  # Left
                        self.set_cell(x - 1, y, self.get_wall_sprite((x - 1, y)))
                    if x + 1 < self.width and self.cell_contains(x + 1, y,".") is None and self.cell_contains(x - 1, y,Entities.Actor) is None:  # Right
                        self.set_cell(x + 1, y, self.get_wall_sprite((x + 1, y)))
                    if y - 1 >= 0 and self.cell_contains(x, y - 1,".") is None and self.cell_contains(x - 1, y,Entities.Actor) is None:  # Top
                        self.set_cell(x, y - 1, self.get_wall_sprite((x, y - 1)))
                    if y + 1 < self.height and self.cell_contains(x, y + 1,".") is None and self.cell_contains(x - 1, y,Entities.Actor) is None:  # Bottom
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
            self.set_cell(x,y, "bw")
            cell = self.grid[y][x]
            if "r" and "." in cell:
                self.remove_from_cell(x,y,"bw")

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

    def remove_from_cell(self,x,y, actor):
        if 0 <= x < self.width and 0 <= y < self.height:
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
        floor = pygame.image.load("Assets/Sprites/Entities/MapAssets/Decor/floor.png")
        rubble = pygame.image.load("Assets/Sprites/Entities/MapAssets/Decor/rubble.png")
        dust = pygame.image.load("Assets/Sprites/Entities/MapAssets/Decor/dust.png")
        garbage = pygame.image.load("Assets/Sprites/Entities/MapAssets/Decor/garbage.png")
        bridge_n = pygame.image.load("Assets/Sprites/Entities/MapAssets/Decor/bn.png")
        bridge_w = pygame.image.load("Assets/Sprites/Entities/MapAssets/Decor/bw.png")

        for y in range(self.height):
            for x in range(self.width):
                if visibility_grid[y][x]:
                    rect = pygame.Rect(x * self.cell_size - camera[0], y * self.cell_size - camera[1], self.cell_size,
                                       self.cell_size)
                    cell_values = self.grid[y][x]
                    if cell_values:
                        most_recent_value = cell_values[0]

                        if  '.' in cell_values:
                            surface.blit(floor, rect)
                        if "g" in cell_values:
                            surface.blit(rubble,rect)
                        if "d" in cell_values:
                            surface.blit(dust,rect)
                        if "j" in cell_values:
                            surface.blit(garbage, rect)
                        if "y" in cell_values:
                            pygame.draw.rect(surface, (0, 0, 255), rect)
                        if "bw" in cell_values:
                            surface.blit(bridge_w, rect)
                        if "bn" in cell_values:
                            surface.blit(bridge_n,rect)

                        if isinstance(most_recent_value, Entities.Actor):
                            surface.blit(most_recent_value.icon, rect)

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
