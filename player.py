import pygame
import os
import constants

os.environ['SDL_AUDIODRIVER'] = 'dsp'

class Player:
    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        self.sprite = pygame.image.load('cat.png')
    
    def draw(self, window, tilewidth: int, tileheight: int) -> None:
        """
        Draws the player.
        """
        screenx = self.x * tilewidth
        screeny = self.y * tileheight
        self.sprite = pygame.transform.scale(self.sprite, (tilewidth, tileheight))
        window.blit(self.sprite, (screenx, screeny))
        pygame.display.update()
    
    def process(self, events: list[pygame.event.Event], tilewidth: int, tileheight: int, numrows: int, numcolumns: int) -> None:
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_LEFT:
                self.x -= 1
            if event.key == pygame.K_RIGHT:
                self.x += 1
            if event.key == pygame.K_UP:
                self.y -= 1
            if event.key == pygame.K_DOWN:
                self.y += 1
        
        self.x = max(0, min(self.x, numcolumns - 1))
        self.y = max(0, min(self.y, numrows - 1))

