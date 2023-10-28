import pygame
import sys
import random

# 初始化pygame
pygame.init()

# 设置屏幕宽度和高度
WIDTH, HEIGHT = 640, 640
win = pygame.display.set_mode((WIDTH, HEIGHT))

# 设置颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)  # 添加绿色代表入口

# 迷宫的行列数
ROWS, COLS = 16, 16

# 每个单元格的宽度和高度
WIDTH_CELL = WIDTH // COLS
HEIGHT_CELL = HEIGHT // ROWS

# 初始化迷宫矩阵，1代表墙，0代表路径
maze = [[1 for _ in range(COLS)] for _ in range(ROWS)]


# 生成迷宫
def create_maze():
    # 选择一个起始点
    start_row, start_col = 0, 0  # 这里我们选择左上角作为起始点
    maze[start_row][start_col] = 3  # 3代表入口

    # 用栈来存储路径
    stack = [(start_row, start_col)]

    # 方向
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while stack:
        current_row, current_col = stack[-1]  # 查看当前位置

        # 获取当前位置可以前往的相邻位置
        valid_neighbours = []
        for dr, dc in directions:
            new_row, new_col = current_row + dr, current_col + dc

            # 检查新位置是否在迷宫范围内并且是墙
            if 0 <= new_row < ROWS and 0 <= new_col < COLS and maze[new_row][new_col] == 1:
                # 检查这个相邻位置是否有两个以上的空邻居
                count_empty = 0
                for dr2, dc2 in directions:
                    # 检查相邻位置的相邻位置
                    if 0 <= new_row + dr2 < ROWS and 0 <= new_col + dc2 < COLS and maze[new_row + dr2][new_col + dc2] == 0:
                        count_empty += 1

                # 如果有不止一个空的邻居，则这个方向不是一个有效的方向
                if count_empty < 2:
                    valid_neighbours.append((new_row, new_col))

        if valid_neighbours:
            # 随机选择一个有效的邻居作为下一个点
            next_row, next_col = random.choice(valid_neighbours)
            # 将新位置设为路径，并将其添加到栈中
            maze[next_row][next_col] = 0
            stack.append((next_row, next_col))
        else:
            # 如果没有有效的邻居，我们已经到达“死胡同”，回溯
            stack.pop()

    # 确保有一个出口，我们设定迷宫的右下角为出口
    maze[ROWS - 1][COLS - 1] = 2  # 2表示出口


# 绘制迷宫
def draw_maze():
    win.fill(WHITE)
    for i in range(ROWS):
        for j in range(COLS):
            color = BLACK
            if maze[i][j] == 0:
                color = WHITE
            elif maze[i][j] == 2:
                color = RED
            elif maze[i][j] == 3:
                color = GREEN  # 入口用绿色表示

            pygame.draw.rect(win, color, (j * WIDTH_CELL, i * HEIGHT_CELL, WIDTH_CELL, HEIGHT_CELL))
    pygame.display.update()

def print_maze(maze):
    for row in maze:
        # 将每个数字转换为字符串，并使用空格连接它们
        print(' '.join([str(item) for item in row]))

def main():
    clock = pygame.time.Clock()
    create_maze()

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_maze()

    pygame.quit()
    print_maze(maze)
    sys.exit()


if __name__ == "__main__":
    main()
