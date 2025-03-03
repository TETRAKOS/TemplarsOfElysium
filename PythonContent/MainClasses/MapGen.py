import pygame
import random
import Entities

ROOM_COUNT = 32
ROOM_MIN_SIZE = 7
ROOM_MAX_SIZE = 12

class Grid:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        self.rooms = []

    def generate_dungeon(self):
        self.rooms = []

        for i in range(ROOM_COUNT):
            room_width = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            room_height = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            x = random.randint(1, self.width - room_width - 2)
            y = random.randint(1, self.height - room_height - 2)

            new_room = (x, y, room_width, room_height)
            if any(self.overlap(new_room, r) for r in self.rooms):
                continue
            self.add_room(new_room)
            self.rooms.append(new_room)

        for i in range(1, len(self.rooms)):
            #c_room = self.find_closest_room(self.rooms[i])
            self.connect_rooms(self.rooms[i-1], self.rooms[i])
        self.encase_rooms()

    def get_starting_point(self):
        room = self.rooms[0]
        x = (room[0])
        y = (room[1])
        print(x,y)
        return [x,y]
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
        x1, y1, w1, h1 = new_room
        x2, y2, w2, h2 = existing_room
        return not (x1 + w1 <= x2 or x2 + w2 <= x1 or y1 + h1 <= y2 or y2 + h2 <= y1)

    def add_room(self, room):
        x, y, width, height = room
        for i in range(y, y + height):
            for j in range(x, x + width):
                self.set_cell(j, i, '.')  # Set floor tile

    def encase_rooms(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.get_cell(x, y) == '.':
                    if x - 1 >= 0 and self.get_cell(x - 1, y) is None:  # Left
                        self.set_cell(x - 1, y, self.get_wall_sprite((x - 1, y)))
                    if x + 1 < self.width and self.get_cell(x + 1, y) is None:  # Right
                        self.set_cell(x + 1, y, self.get_wall_sprite((x + 1, y)))
                    if y - 1 >= 0 and self.get_cell(x, y - 1) is None:  # Top
                        self.set_cell(x, y - 1, self.get_wall_sprite((x, y - 1)))
                    if y + 1 < self.height and self.get_cell(x, y + 1) is None:  # Bottom
                        self.set_cell(x, y + 1, self.get_wall_sprite((x, y + 1)))

    def connect_rooms(self, room1, room2):
        x1, y1, _, _ = room1
        x2, y2, _, _ = room2


        edge1 = (random.choice([x1, x1 + room1[2] - 1]), random.choice([y1, y1 + room1[3] - 1]))
        edge2 = (random.choice([x2, x2 + room2[2] - 1]), random.choice([y2, y2 + room2[3] - 1]))

        if random.choice([True, False]):
            self.draw_horizontal_corridor(edge1[0], edge2[0], edge1[1])
            self.draw_vertical_corridor(edge1[1], edge2[1], edge2[0])
        else:
            self.draw_vertical_corridor(edge1[1], edge2[1], edge1[0])
            self.draw_horizontal_corridor(edge1[0], edge2[0], edge2[1])

    def draw_horizontal_corridor(self, x1, x2, y):

        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.set_cell(x, y, '.')  # Set floor tile

    def draw_vertical_corridor(self, y1, y2, x):
        # Draw the corridor
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.set_cell(x, y, '.')  # Set floor tile
    def set_cell(self, x, y, value):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = value

    def get_cell(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None

    def draw(self, surface, camera, visibility_grid):
        for y in range(self.height):
            for x in range(self.width):
                if visibility_grid[y][x]:
                    rect = pygame.Rect(x * self.cell_size - camera[0], y * self.cell_size - camera[1], self.cell_size,
                                       self.cell_size)
                    cell_value = self.grid[y][x]
                    if cell_value == '.':
                        pygame.draw.rect(surface, (50, 50, 50), rect)
                    if isinstance(cell_value, Entities.Actor):
                        surface.blit(cell_value.icon, rect)

    def get_actors(self):
        actors = []
        for y in range(self.height):
            for x in range(self.width):
                cell_value = self.grid[y][x]
                if isinstance(cell_value, Entities.Actor):
                    actors.append(cell_value)
        return actors

    def get_wall_sprite(self, pos):
        x, y = pos
        neighbors = [
            self.get_cell(x - 1, y),  # Left
            self.get_cell(x + 1, y),  # Right
            self.get_cell(x, y - 1),  # Top
            self.get_cell(x, y + 1)    # Bottom
        ]
        if neighbors[0] is not None and neighbors[1] is not None and neighbors[2] is None or '.' and neighbors[3] is None or '.':
            return Entities.Wall(pos, "Assets/Sprites/Entities/MapAssets/Wall/Directional/w_hor_f.png")  # Horizontal long
        #if neighbors[0] and neighbors[1] is Entities.Wall:
        #    return Entities.Wall(pos, "Assets/Sprites/Entities/MapAssets/Wall/Directional/w_center.png") # Center (alone)
        #elif neighbors[0] and neighbors[1] is Entities.Wall:
         #    return Entities.Wall(pos, "Assets/Sprites/Entities/MapAssets/Wall/Directional/w_hor_f.png")
        # elif neighbors[0] is None and neighbors[1] is None and neighbors[2] is not None and neighbors[3] is not None:
        #      return Entities.Wall(pos, "Assets/Sprites/Entities/MapAssets/Wall/Directional/w_corner_dl.png")  # Top corner
        # elif neighbors[0] is None and neighbors[1] is None and neighbors[2] is not None and neighbors[3] is not None:
        #      return Entities.Wall(pos, "Assets/Sprites/Entities/MapAssets/Wall/Directional/w_corner_lu.png")  # Bottom corner
        # elif neighbors[0] is not None and neighbors[1] is not None and neighbors[2] is None and neighbors[3] is None:
        #      return Entities.Wall(pos, "Assets/Sprites/Entities/MapAssets/Wall/Directional/w_corner_dr.png")  # Left corner
        # elif neighbors[0] is not None and neighbors[1] is not None and neighbors[2] is None and neighbors[3] is None:
        #      return Entities.Wall(pos, "Assets/Sprites/Entities/MapAssets/Wall/Directional/w_corner_ur.png")  # Right corner
        # elif all(neighbor is not None for neighbor in neighbors):
        #      return Entities.Wall(pos, "Assets/Sprites/Entities/MapAssets/Wall/Directional/w_full.png")  # Full
        # elif neighbors[0] is not None and neighbors[1] is not None and neighbors[2] is None and neighbors[3] is None:
        #      return Entities.Wall(pos, "Assets/Sprites/Entities/MapAssets/Wall/Directional/w_hor_f.png")  # Horizontal long
        # elif neighbors[0] is None and neighbors[1] is None and neighbors[2] is not None and neighbors[3] is not None:
        #      return Entities.Wall(pos, "Assets/Sprites/Entities/MapAssets/Wall/Directional/w_vert_f.png")  # Vertical long
        # elif neighbors[0] is not None and neighbors[1] is None and neighbors[2] is None and neighbors[3] is not None:
        #      return Entities.Wall(pos, "Assets/Sprites/Entities/MapAssets/Wall/Directional/w_vert_hu.png")  # Vertical end top
        # elif neighbors[0] is None and neighbors[1] is not None and neighbors[2] is not None and neighbors[3] is None:
        #      return Entities.Wall(pos, "Assets/Sprites/Entities/MapAssets/Wall/Directional/w_vert_hd.png")  # Vertical end bottom
        # elif neighbors[0] is not None and neighbors[1] is None and neighbors[2] is not None and neighbors[3] is None:
        #      return Entities.Wall(pos, "Assets/Sprites/Entities/MapAssets/Wall/Directional/w_hor_hl.png")  # Horizontal end left
        # elif neighbors[0] is None and neighbors[1] is not None and neighbors[2] is None and neighbors[3] is not None:
        #      return Entities.Wall(pos, "Assets/Sprites/Entities/MapAssets/Wall/Directional/w_hor_hr.png")  # Horizontal end right
        #    else:
        #    return Entities.Wall(pos, "Assets/Sprites/Entities/MapAssets/Wall/Wall_cnc.png")  # Default
