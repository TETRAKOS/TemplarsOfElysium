import pygame
import random
import Items
import Entities

# Constants
ROOM_COUNT = 10
ROOM_MIN_SIZE = 3
ROOM_MAX_SIZE = 7

class Grid:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        self.rooms = []

    def generate_dungeon(self):
        # Set the outer walls of the dungeon
        for x in range(self.width):
            self.set_cell(x, 0, Entities.Wall((x, 0)))  # Top wall
            self.set_cell(x, self.height - 1, Entities.Wall((x, self.height - 1)))  # Bottom wall
        for y in range(self.height):
            self.set_cell(0, y, Entities.Wall((0, y)))  # Left wall
            self.set_cell(self.width - 1, y, Entities.Wall((self.width - 1, y)))  # Right wall

        self.rooms = []

        for _ in range(ROOM_COUNT):
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
            c_room = self.find_closest_room(self.rooms[i])
            self.connect_rooms(c_room, self.rooms[i])

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


        # for i in range(y - 1, y + height + 1):
        #     if i >= 0 and i < self.height:
        #         if x - 1 >= 0:
        #             self.set_cell(x - 1, i, Entities.Wall((x - 1, i)))  # Left wall
        #         if x + width < self.width:
        #             self.set_cell(x + width, i, Entities.Wall((x + width, i)))  # Right wall
        # for j in range(x - 1, x + width + 1):
        #     if j >= 0 and j < self.width:
        #         if y - 1 >= 0:
        #             self.set_cell(j, y - 1, Entities.Wall((j, y - 1)))  # Top wall
        #         if y + height < self.height:
        #             self.set_cell(j, y + height, Entities.Wall((j, y + height)))  # Bottom wall

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


            #if y - 1 >= 0:
            #     for x in range(min(x1, x2), max(x1, x2) + 1):
            #         self.set_cell(x, y - 1, Entities.Wall((x, y - 1)))  # Top wall
            # if y + 1 < self.height:
            #     for x in range(min(x1, x2), max(x1, x2) + 1):
            #         self.set_cell(x, y + 1, Entities.Wall((x, y + 1)))  # Bottom wall
            # if x1 - 1 >= 0:
            #         self.set_cell(x1 - 1, y, None)  # Left end wall
            # if x2 + 1 < self.width:
            #         self.set_cell(x2 + 1, y, None)

    def draw_vertical_corridor(self, y1, y2, x):
        # Draw the corridor
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.set_cell(x, y, '.')  # Set floor tile

    #     if x - 1 >= 0:
    #         for y in range(min(y1, y2), max(y1, y2) + 1):
    #             self.set_cell(x - 1, y, Entities.Wall((x - 1, y)))  # Left wall
    #     if x + 1 < self.width:
    #         for y in range(min(y1, y2), max(y1, y2) + 1):
    #             self.set_cell(x + 1, y, Entities.Wall((x + 1, y)))  # Right wall
    #     if y1 - 1 >= 0:
    #         self.set_cell(x, y1 - 1, None)  # Top end wall
    #     if y2 + 1 < self.height:
    #         self.set_cell(x, y2 + 1, None)
    #
    def set_cell(self, x, y, value):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = value

    def get_cell(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None

    def draw(self, surface, camera):
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(x * self.cell_size - camera[0], y * self.cell_size - camera[1], self.cell_size,
                                   self.cell_size)
                cell_value = self.grid[y][x]

                # Draw the walls and floors

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

