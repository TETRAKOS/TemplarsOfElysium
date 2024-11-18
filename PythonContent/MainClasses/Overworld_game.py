import pygame


class Grid:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid = [[None for _ in range(width)] for _ in range(height)]

    def set_cell(self, x, y, value):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = value

    def get_cell(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None

    def draw(self, surface):
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(surface, (200, 200, 200), rect, 1)

                cell_value = self.grid[y][x]
                if cell_value == "wall":
                    pygame.draw.rect(surface, (100, 100, 100), rect)
                elif cell_value == "item":
                    pygame.draw.circle(surface, (255, 0, 0), rect.center, self.cell_size // 4)


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
        self.clock = pygame.time.Clock()
        self.grid = Grid(20, 15, 40)
        self.setup_grid()
        self.map_loop()

    def setup_grid(self):
        for i in range(20):
            self.grid.set_cell(i, 0, "wall")
            self.grid.set_cell(i, 14, "wall")
        for i in range(15):
            self.grid.set_cell(0, i, "wall")
            self.grid.set_cell(19, i, "wall")

        self.grid.set_cell(5, 5, "item")
        self.grid.set_cell(10, 10, "item")

    def map_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.surface.fill(self.bgc)  # Fill with white background
            self.grid.draw(self.surface)
            pygame.display.flip()
            self.clock.tick(60)  # Limit to 60 FPS

        pygame.quit()


if __name__ == "__main__":
    Game()

gameloop = Game