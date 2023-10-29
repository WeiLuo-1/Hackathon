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
<<<<<<< HEAD
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
=======

>>>>>>> refs/remotes/origin/main
def main():
    # set up pygame window
    icon = pygame.image.load('trophy.png')
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Maze Challenge")
    window = pygame.display.set_mode((constants.screen_width, constants.screen_height))

    # set up pygame clock
    clock = pygame.time.Clock()

    # ================
    # set up game data
    # ================

    playerdata = player.Player()

    lvl = 1
    
    # 迷宫的行列数
    ROWS,COLS = level.level(lvl)

    # 初始化迷宫矩阵，1代表墙，0代表路径
    mazeData = [[1 for _ in range(COLS)] for _ in range(ROWS)]
    maze.create_maze(mazeData,COLS,ROWS)

    # set up sockets
    serverport = 42000 + random.randint(0, 10) # random port for easier testing
    serversocket = server.start_server('localhost', serverport)
    print(f'started server on port {serverport}')

    clientconnections: list[server.ClientConnection] = [] # list of connections
    inboundmessages: list[str] = [] # queue of messages received
    outboundmessages: list[str] = [] # queue of messages to send

<<<<<<< HEAD
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
=======
    # detect impossible mazes
    while astar(mazeData) == None:
        mazeData = [[1 for _ in range(COLS)] for _ in range(ROWS)]
        maze.create_maze(mazeData, COLS, ROWS)
>>>>>>> refs/remotes/origin/main
    
    path = astar(mazeData)
    print(path)
    print()

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
        if command == constants.COMMAND_GET_STATE:
            m = ''
            for row in mazeData:
                for col in row:
                    m += str(col)
                m += '\n'
            outboundmessages.append(m)
        
        # allow player to interactively send commands (using arrow keys)
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_LEFT:
                command = constants.COMMAND_MOVE_LEFT
            if event.key == pygame.K_RIGHT:
                command = constants.COMMAND_MOVE_RIGHT
            if event.key == pygame.K_UP:
                command = constants.COMMAND_MOVE_UP
            if event.key == pygame.K_DOWN:
                command = constants.COMMAND_MOVE_DOWN

        playerdata.process(command, mazeData, tilewidth, tileheight, ROWS, COLS)

        # ====================
        # update game graphics
        # ====================

        maze.draw_maze(window, mazeData, COLS, ROWS)
        playerdata.draw(window, tilewidth, tileheight)
        pygame.display.update()

        if mazeData[playerdata.y][playerdata.x] == 2:
            lvl += 1
            ROWS,COLS = level.level(lvl)
            mazeData = [[1 for _ in range(COLS)] for _ in range(ROWS)]
            maze.create_maze(mazeData,COLS,ROWS)
            while astar(mazeData) == None:
                mazeData = [[1 for _ in range(COLS)] for _ in range(ROWS)]
                maze.create_maze(mazeData, COLS, ROWS)
            playerdata.x, playerdata.y = 0,0
            path = astar(mazeData)
            print(path)
            print()
        
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
