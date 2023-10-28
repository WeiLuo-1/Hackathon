import pygame
import random
import sys

# 初始化pygame
pygame.init()

# 设置颜色变量
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 迷宫的尺寸
rows, cols = 16,16
cell_size = 32

# 设置屏幕大小
window = pygame.display.set_mode((cols * cell_size, rows * cell_size))
pygame.display.set_caption("随机迷宫生成")

# 创建迷宫数组，初始都是墙
maze = [[1] * cols for _ in range(rows)]

def print_array(arr):
    for row in arr:
        # 这将转换每个元素为字符串，并在它们之间插入空格，形成一行
        print(' '.join(map(str, row)))

# 迷宫单元格的类
class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}
        self.visited = False

    def draw(self, window):
        x = self.col * cell_size
        y = self.row * cell_size
        if self.visited:
            pygame.draw.rect(window, BLUE, (x, y, cell_size, cell_size))

        if self.walls["top"]:
            pygame.draw.line(window, WHITE, (x, y), (x + cell_size, y), 2)
        if self.walls["right"]:
            pygame.draw.line(window, WHITE, (x + cell_size, y), (x + cell_size, y + cell_size), 2)
        if self.walls["bottom"]:
            pygame.draw.line(window, WHITE, (x + cell_size, y + cell_size), (x, y + cell_size), 2)
        if self.walls["left"]:
            pygame.draw.line(window, WHITE, (x, y + cell_size), (x, y), 2)

# 初始化网格
grid = []
for row in range(rows):
    row_cells = []
    for col in range(cols):
        cell = Cell(row, col)
        row_cells.append(cell)
    grid.append(row_cells)

# 移动到随机的相邻单元格
def move_to_next(cell):
    next_cell = None
    directions = ["top", "right", "bottom", "left"]
    random.shuffle(directions)

    for direction in directions:
        r = cell.row
        c = cell.col
        if direction == "top" and r > 0:
            r -= 1
        elif direction == "right" and c < cols - 1:
            c += 1
        elif direction == "bottom" and r < rows - 1:
            r += 1
        elif direction == "left" and c > 0:
            c -= 1

        if grid[r][c].visited is False:
            next_cell = grid[r][c]
            next_cell.visited = True

            # Remove walls
            if direction == "top":
                cell.walls["top"] = next_cell.walls["bottom"] = False
            elif direction == "right":
                cell.walls["right"] = next_cell.walls["left"] = False
            elif direction == "bottom":
                cell.walls["bottom"] = next_cell.walls["top"] = False
            elif direction == "left":
                cell.walls["left"] = next_cell.walls["right"] = False
            break

    return next_cell

# 使用DFS生成迷宫
def generate_maze(cell):
    stack = [cell]
    while stack:
        current = stack[-1]
        current.visited = True
        next_cell = move_to_next(current)

        if next_cell:
            stack.append(next_cell)
        else:
            stack.pop()

# 开始生成迷宫
start_cell = grid[0][0]
generate_maze(start_cell)

# 根据Cell对象的墙的状态更新迷宫数组
for row in range(rows):
    for col in range(cols):
        cell = grid[row][col]
        if not any(cell.walls.values()):  # 如果一个单元格四面都没有墙
            maze[row][col] = 0  # 这表示是一个可行走的路径

# 游戏循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

    window.fill((0, 0, 0))  # 使用黑色清空屏幕

    # 根据maze数组和Cell对象的状态绘制迷宫
    for row in range(rows):
        for col in range(cols):
            cell = grid[row][col]
            cell.draw(window)
            if maze[row][col] == 0:  # 如果是可行走的路径
                x = col * cell_size
                y = row * cell_size
                pygame.draw.rect(window, GREEN, (x, y, cell_size, cell_size))  # 用绿色绘制

    pygame.display.flip()

pygame.quit()
print_array( maze)
