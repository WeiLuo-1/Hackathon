import pygame
import os
import constants

os.environ['SDL_AUDIODRIVER'] = 'dsp'

#draw the player in the screen
def player(playerImg, window, x,y):
    window.blit(playerImg,(x,y))


#Game loop
def move(playerX, playerY, window, event):
    COLS = 16
    player_move = constants.screen_width // COLS
    playerImg = pygame.image.load('cat.png')
    playerImg = pygame.transform.scale(playerImg, (player_move, player_move))
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            playerX -= player_move
        if event.key == pygame.K_RIGHT:
            playerX += player_move
        if event.key == pygame.K_UP:
            playerY -= player_move
        if event.key == pygame.K_DOWN:
            playerY += player_move
    playerX = max(0, min(playerX, constants.screen_width-playerImg.get_width()))
    playerY = max(0, min(playerY, constants.screen_height-playerImg.get_height()))

    player(playerImg, window, playerX,playerY)
    pygame.display.update()
