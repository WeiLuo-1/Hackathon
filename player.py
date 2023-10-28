import pygame
import os
import constants

os.environ['SDL_AUDIODRIVER'] = 'dsp'

#draw the player in the screen
def player(playerImg, window, x,y):
    window.blit(playerImg,(x,y))


#Game loop
def move(window, event):
    playerImg = pygame.image.load('cat.png')
    playerX = 0
    playerY = 0
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            playerX -= constants.player_move
        if event.key == pygame.K_RIGHT:
            playerX += constants.player_move
        if event.key == pygame.K_UP:
            playerY -= constants.player_move
        if event.key == pygame.K_DOWN:
            playerY += constants.player_move
    playerX = max(0, min(playerX, 1280-playerImg.get_width()))
    playerY = max(0, min(playerY, 720-playerImg.get_height()))

    player(playerImg, window, playerX,playerY)
    pygame.display.update()
