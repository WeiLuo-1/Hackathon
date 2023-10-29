import pygame
import random
import constants

def create_maze(maze, COLS, ROWS):
    # Initialize all cells of the maze to 0
    for row in range(ROWS):
        for col in range(COLS):
            maze[row][col] = 0

    # Create the maze using recursive division
    divide_region(maze, 0, 0, COLS, ROWS, "H" if random.random() < 0.5 else "V")

    # Set the entrance and exit
    maze[0][0] = 3  # Entrance
    maze[ROWS - 1][COLS - 1] = 2  # Exit

# Draw the maze
def draw_maze(window, maze, COLS, ROWS):
    WIDTH_CELL = constants.tileWidth
    HEIGHT_CELL = constants.tileHeight
    window.fill(constants.WHITE)
    for i in range(ROWS):
        for j in range(COLS):
            color = constants.BLACK
            if maze[i][j] == 0:
                color = constants.WHITE
            elif maze[i][j] == 2:
                color = constants.RED
            elif maze[i][j] == 3:
                color = constants.GREEN  # Green for the entrance

            pygame.draw.rect(window, color, (j * WIDTH_CELL, i * HEIGHT_CELL, WIDTH_CELL, HEIGHT_CELL))
    # pygame.display.update()

def print_maze(maze):
    for row in maze:
        # Convert each number to a string and join them with a space
        print(' '.join([str(item) for item in row]))

def divide_region(maze, x, y, width, height, orientation):
    # Stop when the region becomes smaller than the minimum dividable size
    MIN_SIZE = 2
    if width <= MIN_SIZE or height <= MIN_SIZE:
        return

    horizontal = orientation == "H"

    # Division if it's horizontal
    if horizontal:
        wall_x = random.randrange(x + 1, x + width - 1)  # Randomly select the position of the wall
        passage = random.randrange(y, y + height)  # Randomly select the position of the passage
        for i in range(y, y + height):
            if i == passage:  # Leave a space for the passage
                continue
            maze[i][wall_x] = 1  # Place walls in other positions

        # Recursively divide the new regions
        divide_region(maze, x, y, wall_x - x, height, "V")
        divide_region(maze, wall_x + 1, y, x + width - wall_x - 1, height, "V")

    # Division if it's vertical
    else:
        wall_y = random.randrange(y + 1, y + height - 1)  # Randomly select the position of the wall
        passage = random.randrange(x, x + width)  # Randomly select the position of the passage
        for i in range(x, x + width):
            if i == passage:  # Leave a space for the passage
                continue
            maze[wall_y][i] = 1  # Place walls in other positions

        # Recursively divide the new regions
        divide_region(maze, x, y, width, wall_y - y, "H")
        divide_region(maze, x, wall_y + 1, width, y + height - wall_y - 1, "H")
