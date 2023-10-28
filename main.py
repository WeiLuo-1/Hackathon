import pygame
import sys
import maze
import constants
import random
import player
import server
from bot import astar 

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
    # set up sockets
    serverport = 42000 + random.randint(0, 10) # random port for easier testing
    serversocket = server.start_server('localhost', serverport)
    print(f'started server on port {serverport}')

    clientconnections: list[sever.ClientConnection] = [] # list of connections

    # set up game data
    playerdata = player.Player()

    # 设置屏幕宽度和高度
  
    maze.create_maze(mazeData, COLS, ROWS)
    path = astar(mazeData)
    print(path)

    running = True
    while running:
        clock.tick(60)

        # listen for new socket connections
        s = server.accept_connection(serversocket)
        if not s is None:
            clientconnections.append(s)
            print(f'client connected')

        # get pygame events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        tilewidth = constants.screen_width // COLS
        tileheight = constants.screen_height // ROWS

        # update game logic
        playerdata.process(events, mazeData, tilewidth, tileheight, ROWS, COLS)

        # update game graphics
        maze.draw_maze(window, mazeData, COLS, ROWS)
        playerdata.draw(window, tilewidth, tileheight)
        pygame.display.update()

        if mazeData[playerdata.y][playerdata.x] == 2:
            running = False
            print("YOU WIN")
        
    pygame.quit()
    # maze.print_maze(mazeData)
    sys.exit()


if __name__ == "__main__":
    main()
