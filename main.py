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
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("space invaders")

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
    
    # ==============
    # set up sockets
    # ==============

    serverport = 42000 + random.randint(0, 10) # random port for easier testing
    serversocket = server.start_server('localhost', serverport)
    print(f'started server on port {serverport}')

    clientconnections: list[sever.ClientConnection] = [] # list of connections
    inboundmessages: list[str] = [] # queue of messages received
    outboundmessages: list[str] = [] # queue of messages to send

    # ================
    # set up game data
    # ================

    playerdata = player.Player()

    # 设置屏幕宽度和高度
    
    # make sure the cells next to the exit not blocked
    while mazeData[ROWS-2][COLS-1] == 1 and mazeData[ROWS-1][COLS-2] == 1:
        mazeData = [[1 for _ in range(COLS)] for _ in range(ROWS)]
        maze.create_maze(mazeData, COLS, ROWS)
        print("regenerate")

    
    path = astar(mazeData)
    print(path)

    running = True
    while running:
        clock.tick(60)

        # =======
        # netcode
        # =======

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

        # =================
        # update game logic
        # =================

        command = ''
        if len(inboundmessages) > 0:
            command = inboundmessages.pop(0)
        if command == 'get_gamestate':
            m = ''
            for row in mazeData:
                for col in row:
                    m += str(col)
                m += '\n'
            outboundmessages.append(m)

        playerdata.process(events, mazeData, tilewidth, tileheight, ROWS, COLS)

        if mazeData[playerdata.y][playerdata.x] == 2:
            lvl += 1
            ROWS,COLS = level.level(lvl)
            mazeData = [[1 for _ in range(COLS)] for _ in range(ROWS)]
            maze.create_maze(mazeData,COLS,ROWS)
            playerdata.x, playerdata.y = 0,0
        
        # ====================
        # update game graphics
        # ====================
        maze.draw_maze(window, mazeData, COLS, ROWS)
        playerdata.draw(window, tilewidth, tileheight)
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
