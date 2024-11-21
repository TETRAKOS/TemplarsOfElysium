#import numpy
import pygame
from Entities import Player, Hostile, Actor, Wall, Loot
from UIElements import Rectangle, TextRenderer
import Shaders
import Items



class Grid:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid = [[None for _ in range(width)] for _ in range(height)]

    def set_cell(self, x, y, value):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = value
          #  print(self.grid[y][x])

    def get_cell(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None

    def draw(self, surface, camera):
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(x * self.cell_size - camera[0], y * self.cell_size - camera[1], self.cell_size,
                                   self.cell_size)
                pygame.draw.rect(surface, (12, 43, 17), rect, 1)

                cell_value = self.grid[y][x]
                if isinstance(cell_value, Actor):
                    surface.blit(cell_value.icon, rect)
    def get_actors(self):
        actors = []
        for y in range(self.height):
            for x in range(self.width):
                cell_value = self.grid[y][x]
                if isinstance(cell_value, Actor):
                    actors.append(cell_value)
        return actors

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
      #  self.gradient = Shaders.generate_gradient((45, 48, 44),(0,0,0),1024,724)
        center = (self.surface.get_width() // 2, self.surface.get_height() // 2)
        radius = 500#min(self.surface.get_width(), self.surface.get_height()) // 2
       # self.gradient = Shaders.generate_radial_gradient(center, radius, self.bgc, self.bgcd, self.surface.get_height(),
       #                                          self.surface.get_width())
       # self.gradient = numpy.transpose(self.gradient, (1, 0, 2))
        self.camera = [0, 0]
        self.clock = pygame.time.Clock()
        self.grid = Grid(20, 25, 40)
        self.setup_grid()
        self.player_pos = [10, 2]
        self.player = Player((self.player_pos[0] * self.grid.cell_size, self.player_pos[1] * self.grid.cell_size),
                             "Assets/Sprites/Entities/Creatures/Player/fig1.png",self)

        self.grid.set_cell(self.player_pos[0], self.player_pos[1], self.player)
        self.enemy = Hostile((5 * self.grid.cell_size, 5 * self.grid.cell_size), "Assets/Sprites/Entities/Creatures/Walker/walker.png")
        self.grid.set_cell(5, 5, Hostile((5,5),"Assets/Sprites/Entities/Creatures/Walker/walker.png"))

        self.turn_count = 0
        self.is_player_turn = True

        self.map_loop()

    def setup_grid(self):
        for i in range(25):
            self.grid.set_cell(i, 0, Wall((i * self.grid.cell_size, 0)))
            self.grid.set_cell(i, 24, Wall((i * self.grid.cell_size, 0)))
        for i in range(15):
            self.grid.set_cell(0, i, Wall((i * self.grid.cell_size, 0)))
            self.grid.set_cell(19, i, Wall((i * self.grid.cell_size, 0)))

        self.grid.set_cell(7, 7, Loot((5,5),"Assets/Sprites/Entities/MapAssets/Loot/Bag/Bag.png"))
        self.grid.set_cell(10, 10, Loot((10,10),"Assets/Sprites/Entities/MapAssets/Loot/Bag/Bag.png"))

    def map_loop(self):
        backdrop = Rectangle(((self.surface.get_width() - 200), 0), (200, self.surface.get_height()), (70, 70, 70))
        turn_text = TextRenderer(self.font_small, (255, 255, 255))
        weapon_icon = pygame.image.load("Assets/Sprites/Icons/Empty.png")
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if self.is_player_turn:  # Only handle input if it's the player's turn
                    move = self.player.handle_input(event)
                    if move != (0, 0):
                        self.move_player(move)
                        self.is_player_turn = False  # End player's turn after moving
                        self.turn_count += 1  # Increment turn count
                        self.handle_enemy_turn()  # Call enemy turn logic


            self.surface.fill(self.bgc)
            self.update_camera()
            clock = pygame.time.Clock()
            fps = str(clock.tick(60))
            pygame.display.set_caption("Templars of Elysium - Map" + fps)
            self.grid.draw(self.surface, self.camera)


            backdrop.draw(self.surface)
            mouse_pos = pygame.mouse.get_pos()

            tile_x = (mouse_pos[0] + self.camera[0]) // self.grid.cell_size
            tile_y = (mouse_pos[1] + self.camera[1]) // self.grid.cell_size

            actor = self.grid.get_cell(tile_x, tile_y)
            if isinstance(actor, Actor):
                info_text = actor.getinfo()
                text_surface = self.font_ann.render(info_text, True, (255, 255, 255))
                text_rect = text_surface.get_rect(topleft=(mouse_pos[0] + 10, mouse_pos[1] + 10))
                self.surface.blit(text_surface, text_rect)
                if isinstance(actor, Loot):
                    pygame.mouse.set_cursor(pygame.cursors.ball)
                if isinstance(actor, Hostile):
                    pygame.mouse.set_cursor(pygame.cursors.diamond)
                    distance_x = abs(self.player_pos[0] - tile_x)
                    distance_y = abs(self.player_pos[1] - tile_y)
                    c_info = max(distance_x, distance_y)
                    c_text = f"Distance: {c_info} cells"
                    text_surface = self.font_small.render(c_text, True, (255, 255, 255))
                    text_rect = text_surface.get_rect(
                        topleft=(mouse_pos[0] + 10, mouse_pos[1] + 30))
                    self.surface.blit(text_surface, text_rect)
            else:
                pygame.mouse.set_cursor(pygame.cursors.arrow)
            #UI
            turn_message = "Your Turn" if self.is_player_turn else "Enemy's Turn"
            turn_text.draw_text(self.surface, turn_message, ((self.surface.get_width() - 150), 50), 100)
            if isinstance(self.player.weapon, Items.Weapon):

            pygame.display.flip()
            self.clock.tick(60)
# 1151 > 1200
        pygame.quit()
    def pass_turn(self):
        print("Turn passed")
        self.is_player_turn = not self.is_player_turn
    def handle_enemy_turn(self):
        print("Enemy's turn")
        self.is_player_turn = True

    def update_camera(self):
        self.camera[0] = self.player_pos[0] * self.grid.cell_size - self.surface.get_width() // 2 + self.grid.cell_size // 2
        self.camera[1] = self.player_pos[1] * self.grid.cell_size - self.surface.get_height() // 2 + self.grid.cell_size // 2

    def move_player(self, move):
        new_x = self.player_pos[0] + move[0]
        new_y = self.player_pos[1] + move[1]
        if not isinstance(self.grid.get_cell(new_x, new_y), Actor):
            self.grid.set_cell(self.player_pos[0], self.player_pos[1], None)  # Clear old position
            self.player_pos = [new_x, new_y]
            self.grid.set_cell(new_x, new_y, self.player)
            self.player.rect.topleft = (new_x * self.grid.cell_size, new_y * self.grid.cell_size)

if __name__ == "__main__":
    Game()

gameloop = Game