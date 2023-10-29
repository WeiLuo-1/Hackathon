import pygame
import random
import constants


# 生成迷宫
def create_maze(maze, COLS, ROWS):
    # 选择一个起始点
    start_row, start_col = 0, 0  # 这里我们选择左上角作为起始点
    maze[start_row][start_col] = 3  # 3代表入口

    # 用栈来存储路径
    stack = [(start_row, start_col)]

    # 方向
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while stack:
        current_row, current_col = stack[-1]  # View current location

        # Get the adjacent locations that the current location can go to
        valid_neighbours = []
        for dr, dc in directions:
            new_row, new_col = current_row + dr, current_col + dc

            # Check if the new location is within the maze and is a wall
            if 0 <= new_row < ROWS and 0 <= new_col < COLS and maze[new_row][new_col] == 1:
                # Check whether this adjacent position has more than two empty neighbors
                count_empty = 0
                for dr2, dc2 in directions:
                    # Check adjacent locations for adjacent locations
                    if 0 <= new_row + dr2 < ROWS and 0 <= new_col + dc2 < COLS and maze[new_row + dr2][new_col + dc2] == 0:
                        count_empty += 1

                # This direction is not a valid direction if there is more than one empty neighbor
                if count_empty < 2:
                    valid_neighbours.append((new_row, new_col))

        if valid_neighbours:
            # Randomly select a valid neighbor as the next point
            next_row, next_col = random.choice(valid_neighbours)
            # Set the new location to the path and add it to the stack
            maze[next_row][next_col] = 0
            stack.append((next_row, next_col))
        else:
            # If there are no valid neighbors, we have reached a "dead end" and backtrack
            stack.pop()

    # Make sure there is an exit. We set the lower right corner of the maze as the exit.
    maze[ROWS - 1][COLS - 1] = 2  # 2 means export


# draw maze
def draw_maze(window,maze, COLS, ROWS):
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
                color = constants.GREEN  # 入口用绿色表示

            pygame.draw.rect(window, color, (j * WIDTH_CELL, i * HEIGHT_CELL, WIDTH_CELL, HEIGHT_CELL))
    # pygame.display.update()

def print_maze(maze):
    for row in maze:
        # 将每个数字转换为字符串，并使用空格连接它们
        print(' '.join([str(item) for item in row]))

