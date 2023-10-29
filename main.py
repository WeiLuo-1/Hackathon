import pygame
import sys
import maze
import constants
import random
import player
import server
from bot import astar 
import level

pygame.init()
# 迷宫的行列数
lvl = 1


ROWS,COLS = level.level(lvl)

#caption and window Icon
icon = pygame.image.load('trophy.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("Maze Challenge")

# 每个单元格的宽度和高度


# 初始化迷宫矩阵，1代表墙，0代表路径
mazeData = [[1 for _ in range(COLS)] for _ in range(ROWS)]
maze.create_maze(mazeData,COLS,ROWS)
window = pygame.display.set_mode((constants.screen_width, constants.screen_height))
clock = pygame.time.Clock()
def main():
    
    global lvl
    global mazeData
    global COLS,ROWS

    # set up sockets
    serverport = 42000 + random.randint(0, 10) # random port for easier testing
    serversocket = server.start_server('localhost', serverport)
    print(f'started server on port {serverport}')

    clientconnections: list[sever.ClientConnection] = [] # list of connections
    inboundmessages: list[str] = [] # queue of messages received
    outboundmessages: list[str] = [] # queue of messages to send

    # set up game data
    playerdata = player.Player()

    # 设置屏幕宽度和高度
  
    num_none = 0
    num_test = 100
    for i in range(num_test):
        mazeData = [[1 for _ in range(COLS)] for _ in range(ROWS)]
        maze.create_maze(mazeData, COLS, ROWS)
        if astar(mazeData) is None:
            num_none += 1  

    print("Num none", num_none)

    while astar(mazeData) == None:
        mazeData = [[1 for _ in range(COLS)] for _ in range(ROWS)]
        maze.create_maze(mazeData, COLS, ROWS)  
    
    path = astar(mazeData)
    print(path)
    print()

    running = True
    while running:
        clock.tick(60)

        # listen for new socket connections
        s = server.accept_connection(serversocket)
        if not s is None:
            cc = server.ClientConnection(s)
            clientconnections.append(cc)
            print(f'client connected')
        
        # update sockets
        for cc in clientconnections:
            cc.process()
        
        # receive data from sockets
        inboundmessages.clear() # clear messages from last gameloop
        for cc in clientconnections:
            ms = cc.get_messages()
            inboundmessages.extend(ms) # add received messages to queue
        for m in inboundmessages:
            print(m)
        
        # send data to sockets
        for cc in clientconnections:
            for m in outboundmessages:
                cc.send_message(m)
        outboundmessages.clear()

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
            lvl += 1
            ROWS,COLS = level.level(lvl)
            mazeData = [[1 for _ in range(COLS)] for _ in range(ROWS)]
            maze.create_maze(mazeData,COLS,ROWS)
            playerdata.x, playerdata.y = 0,0
            path = astar(mazeData)
            print(path)
            print()
        
    pygame.quit()
    # maze.print_maze(mazeData)
    sys.exit()


if __name__ == "__main__":
    main()
