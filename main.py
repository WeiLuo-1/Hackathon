import pygame
import sys
import maze
import constants
import random
import player


pygame.init()
# 迷宫的行列数
ROWS, COLS = 16, 16

#caption and window Icon
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("space invaders")

# 每个单元格的宽度和高度


# 初始化迷宫矩阵，1代表墙，0代表路径
mazeData = [[1 for _ in range(COLS)] for _ in range(ROWS)]

window = pygame.display.set_mode((constants.screen_width, constants.screen_height))
clock = pygame.time.Clock()
def main():
    playerdata = player.Player()

    # 设置屏幕宽度和高度
  
    maze.create_maze(mazeData, COLS, ROWS)

    running = True
    while running:
        clock.tick(60)
        maze.draw_maze(window, mazeData, COLS, ROWS)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        tilewidth = constants.screen_width // COLS
        tileheight = constants.screen_height // ROWS

        playerdata.process(events, tilewidth, tileheight, ROWS, COLS)
        playerdata.draw(window, tilewidth, tileheight)
        # pygame.display.update()
        
    pygame.quit()
    maze.print_maze(mazeData)
    sys.exit()


if __name__ == "__main__":
    main()
