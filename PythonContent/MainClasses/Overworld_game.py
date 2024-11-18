import pygame
from Entities import Player, Hostile, Actor, Wall
from UIElements import Rectangle, TextRenderer



class Grid:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid = [[None for _ in range(width)] for _ in range(height)]

    def set_cell(self, x, y, value):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = value
            print(self.grid[y][x])

    def get_cell(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None

    def draw(self, surface, camera):
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(x * self.cell_size - camera[0], y * self.cell_size - camera[1], self.cell_size,
                                   self.cell_size)
                pygame.draw.rect(surface, (200, 200, 200), rect, 1)

                cell_value = self.grid[y][x]
                if isinstance(cell_value, Actor):
                    surface.blit(cell_value.icon, rect)

class Game:
    def __init__(self):
        pygame.init()
        self.font = pygame.font.Font('Assets/fonts/Game/HomeVideo-Regular.otf', 32)
        self.font_small = pygame.font.Font('Assets/fonts/Game/HomeVideo-Regular.otf', 16)
        self.gameIcon = pygame.image.load("Assets/Sprites/icons/Icon33.png")
        pygame.display.set_icon(self.gameIcon)
        pygame.display.set_caption("Templars of Elysium - Map")
        self.surface = pygame.display.set_mode((1024, 600))
        self.bgc = (45, 48, 44)
        self.camera = [0, 0]
        self.clock = pygame.time.Clock()
        self.grid = Grid(20, 25, 40)
        self.setup_grid()
        self.player_pos = [10, 2]
        self.player = Player((self.player_pos[0] * self.grid.cell_size, self.player_pos[1] * self.grid.cell_size),
                             "Assets/Sprites/Entities/Creatures/Player/fig1.png")

        self.grid.set_cell(self.player_pos[0], self.player_pos[1], self.player)  # Mark the player's position on the grid
        self.enemy = Hostile((5 * self.grid.cell_size, 5 * self.grid.cell_size), "Assets/Sprites/Entities/Creatures/Walker/walker.png")
        self.grid.set_cell(5, 5, "enemy")  # Mark the enemy's position on the grid

        self.turn_count = 0  # Initialize turn count
        self.is_player_turn = True

        self.map_loop()

    def setup_grid(self):
        for i in range(25):
            self.grid.set_cell(i, 0, Wall((i * self.grid.cell_size, 0)))
            self.grid.set_cell(i, 24, Wall((i * self.grid.cell_size, 0)))
        for i in range(15):
            self.grid.set_cell(0, i, Wall((i * self.grid.cell_size, 0)))
            self.grid.set_cell(19, i, Wall((i * self.grid.cell_size, 0)))

        self.grid.set_cell(5, 5, "item")
        self.grid.set_cell(10, 10, "item")

    def map_loop(self):
        backdrop = Rectangle(((self.surface.get_width() - 200), 0), (200, self.surface.get_height()), (70, 70, 70))
        turn_text = TextRenderer(self.font_small, (255, 255, 255))
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
            self.grid.draw(self.surface, self.camera)  # Pass camera position to draw method
    #        self.surface.blit(self.player.icon,
    #                          (self.player.rect.x - self.camera[0], self.player.rect.y - self.camera[1]))

            backdrop.draw(self.surface)

            turn_message = "Your Turn" if self.is_player_turn else "Enemy's Turn"
            turn_text.draw_text(self.surface, turn_message, ((self.surface.get_width() - 150), 50), 100)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def handle_enemy_turn(self):
        print("Enemy's turn")
        self.is_player_turn = True

    def update_camera(self):
        self.camera[0] = self.player_pos[0] * self.grid.cell_size - self.surface.get_width() // 2 + self.grid.cell_size // 2
        self.camera[1] = self.player_pos[1] * self.grid.cell_size - self.surface.get_height() // 2 + self.grid.cell_size // 2

    def move_player(self, move):
        new_x = self.player_pos[0] + move[0]
        new_y = self.player_pos[1] + move[1]
        if not isinstance(self.grid.get_cell(new_x, new_y), Actor):# and self.grid.get_cell(new_x, new_y) !=Actor:
            self.grid.set_cell(self.player_pos[0], self.player_pos[1], None)  # Clear old position
            self.player_pos = [new_x, new_y]
            self.grid.set_cell(new_x, new_y, self.player)
            self.player.rect.topleft = (new_x * self.grid.cell_size, new_y * self.grid.cell_size)

if __name__ == "__main__":
    Game()

gameloop = Game