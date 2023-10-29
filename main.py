import pygame
import sys
import maze
import constants
import random
import player
import server
from bot import astar 
import level
import time
from scorebar import ScoreBar
pygame.init()
lvl = 1


ROWS,COLS = level.level(lvl)

#caption and window Icon
icon = pygame.image.load('trophy.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("Maze Challenge")

# 每个单元格的宽度和高度


def main():
    scorebar = ScoreBar()
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

    playerdata = player.Player(pygame.image.load('cat.png'))
    aiData = player.Player(pygame.image.load('ai.png'))

    lvl = 1
    
    # 迷宫的行列数
    ROWS,COLS = level.level(lvl)

    # 初始化迷宫矩阵，1代表墙，0代表路径
    mazeData = [[1 for _ in range(COLS)] for _ in range(ROWS)]
    maze.create_maze(mazeData,COLS,ROWS)

    # set up sockets
    # serverport = 42000 + random.randint(0, 10) # random port for easier testing
    serverport = 42000
    serversocket = server.start_server('localhost', serverport)
    print(f'started server on port {serverport}')

    clientconnections: list[server.ClientConnection] = [] # list of connections
    inboundmessages: list[str] = [] # queue of messages received
    outboundmessages: list[str] = [] # queue of messages to send
    # detect impossible mazes
    while astar(mazeData, aiData.x, aiData.y) == None:
        mazeData = [[1 for _ in range(COLS)] for _ in range(ROWS)]
        maze.create_maze(mazeData, COLS, ROWS)  
    
    path = astar(mazeData, aiData.x, aiData.y)
    running = True

    human_steps = 0
    ai_steps = 0
    is_human_turn = True
    human_reached_goal = False
    ai_reached_goal = False
    ai_turn = False

    while running:
        
        clock.tick(60)

        # =======
        # netcode
        # =======

        # listen for new socket connections
        if ai_turn:
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
        if ai_turn:
            for cc in clientconnections:
                for m in outboundmessages:
                    cc.send_message(m)
            outboundmessages.clear()
        #draw the score bar
       
        # get pygame events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        tilewidth = constants.tileWidth
        tileheight = constants.tileHeight

        # =================
        # update game logic
        # =================

        ai_command = ''
        if ai_turn:
            if len(inboundmessages) > 0:
                ai_command = inboundmessages.pop(0)
            if ai_command == constants.COMMAND_GET_STATE:
                m = f'{aiData.x} {aiData.y} {COLS} '
                for row in mazeData:
                    for col in row:
                        m += str(col)
                m += '\n'
                outboundmessages.append(m)
        player_command = ''
        # allow player to interactively send commands (using arrow keys)
        if not human_reached_goal:
            for event in events:
                if event.type != pygame.KEYDOWN:
                    continue
                if event.key == pygame.K_LEFT:
                    player_command = constants.COMMAND_MOVE_LEFT
                    human_steps += 1
                if event.key == pygame.K_RIGHT:
                    player_command = constants.COMMAND_MOVE_RIGHT
                    human_steps += 1
                if event.key == pygame.K_UP:
                    player_command = constants.COMMAND_MOVE_UP
                    human_steps += 1
                if event.key == pygame.K_DOWN:
                    player_command = constants.COMMAND_MOVE_DOWN
                    human_steps += 1

        playerdata.process(player_command, mazeData, tilewidth, tileheight, ROWS, COLS)
        if not ai_reached_goal:
            aiData.process(ai_command, mazeData, tilewidth, tileheight, ROWS, COLS)

        # ====================
        # update game graphics
        # ====================

        maze.draw_maze(window, mazeData, COLS, ROWS)
        playerdata.draw(window, tilewidth, tileheight)
        aiData.draw(window, tilewidth, tileheight)
        pygame.display.update()
        
        if mazeData[playerdata.y][playerdata.x] == 2:
            human_reached_goal = True
            ai_turn = True
        if mazeData[aiData.y][aiData.x] == 2:
            ai_reached_goal = True
        if human_reached_goal and ai_reached_goal:
            ai_steps = len(path) - 1
            print(human_steps)
            print(ai_steps)
            if human_steps <= ai_steps:  # player wins or ties
                scorebar.increase_human_score()
                message = "Player Wins!" if human_steps < ai_steps else "It's a Tie!"
            else:  # AI wins
                scorebar.increase_ai_score()
                message = "AI Wins!"
            human_steps = 0
            ai_steps = 0
            human_reached_goal = False
            ai_reached_goal = False    
            lvl += 1
            ROWS,COLS = level.level(lvl)
            mazeData = [[1 for _ in range(COLS)] for _ in range(ROWS)]
            maze.create_maze(mazeData,COLS,ROWS)
            while astar(mazeData, aiData.x, aiData.y) == None:
                mazeData = [[1 for _ in range(COLS)] for _ in range(ROWS)]
                maze.create_maze(mazeData, COLS, ROWS)
            playerdata.x, playerdata.y = 0,0
            aiData.x,aiData.y = 0,0
            path = astar(mazeData, aiData.x, aiData.y)
            ai_turn = False

            
        
        scorebar.draw(window)
        pygame.display.update()
       

    pygame.quit()
    sys.exit()

    pygame.display.update()

if __name__ == "__main__":
    main()
