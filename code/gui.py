import pygame

class QueensGUI:

    _colors = {
        'v': (158, 161, 212),  # violet 
        'g': (197, 235, 170),  # green 
        'r': (253, 138, 138),  # red 
        'o': (255, 190, 152),  # orange
        'b': (90, 178, 255),   # blue 
        'p': (228, 147, 179),  # pink
        'y': (255, 249, 208),  # yellow 
        't': (168, 209, 209)   # teal blue 
    }

    """
    Initializes graphics variables. 

    Args:
        grid (list[list[str]]): The grid represented as a 2D list of color codes (strings).
        queens (list[tuple[int, int]]): A list of tuples containing queen positions on game board or empty list.
    
    Returns:
        None
    """
    def __init__(self, grid, queens: list[tuple[int, int]]) -> None:
        self._grid = grid
        self._queens = queens

        pygame.init()

        self._GRID_WIDTH = len(self._grid)
        self._GRID_HEIGHT = len(self._grid[0])
        self._CELL_SIZE = 50

        SCREEN_WIDTH = self._GRID_WIDTH * self._CELL_SIZE
        SCREEN_HEIGHT = self._GRID_HEIGHT * self._CELL_SIZE

        self._screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Queens")



    """
    Draws circle on screen.

    Args:
        x (float): X postion of circle.
        y (float): Y postion of circle.
        radius (float): Circle radius.
        color (tuple): RGB color of circle.
    
    Returns:
        None
    """
    def _draw_circle(self, x, y, radius, color=(0, 0, 0)) -> None:
        pygame.draw.circle(
            self._screen, 
            color, 
            [x, y],#[x * self._CELL_SIZE + self._CELL_SIZE / 2, y * self._CELL_SIZE + self._CELL_SIZE / 2], 
            radius, # self._CELL_SIZE / 3, 
            1
        )


    """
    Draws queens as circles on screen.

    Args:
        None
    
    Returns:
        None
    """
    def _draw_queens(self) -> None:
        for x, y in self._queens:
            for i in range(5):
                self._draw_circle(
                    x * self._CELL_SIZE + self._CELL_SIZE / 2,
                    y * self._CELL_SIZE + self._CELL_SIZE / 2,
                    self._CELL_SIZE / 3 - (i * 3),
                   (0, 0, 0)
                )


    """
    Draws gameboard on screen.

    Args:
        None
    
    Returns:
        None
    """
    def _draw_grid(self) -> None:
        for x in range(self._GRID_WIDTH):
            for y in range(self._GRID_HEIGHT):
                color = self._colors[self._grid[y][x]]
                pygame.draw.rect(self._screen, color, (x * self._CELL_SIZE, y * self._CELL_SIZE, self._CELL_SIZE, self._CELL_SIZE))
                pygame.draw.rect(self._screen, (0, 0, 0), (x * self._CELL_SIZE, y * self._CELL_SIZE, self._CELL_SIZE, self._CELL_SIZE), 1)


    """
    Drwas graphics on a screen in a loop. 

    Args:
        None
    
    Returns:
        None
    """
    def main(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self._screen.fill((0, 0, 0))  
            self._draw_grid()
            self._draw_queens()
            pygame.display.flip()

        pygame.quit()