import pygame
import os
import constant
os.environ['SDL_AUDIODRIVER'] = 'dsp'

#intialize the pygame
pygame.init()

#create the screen 
screen = pygame.display.set_mode((constant.screen_width,constant.screen_height))

#caption and window Icon
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("space invaders")

#Player 
playerImg = pygame.image.load('cat.png')
playerX = 0
playerY = 0

constant.player_move = 16

#draw the player in the screen
def player(x,y):
    screen.blit(playerImg,(x,y))


#Game loop
running = True
while running:
    #RGB = red, green, blue
    screen.fill((0,0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX -= constant.player_move
            if event.key == pygame.K_RIGHT:
                playerX += constant.player_move
            if event.key == pygame.K_UP:
                playerY -= constant.player_move
            if event.key == pygame.K_DOWN:
                playerY += constant.player_move
            playerX = max(0, min(playerX, 1280))
            playerY = max(0, min(playerY, 720))

               
    
    player(playerX,playerY)

    
    pygame.display.update()
pygame.quit()