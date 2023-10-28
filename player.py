import pygame
import os

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
    
    def process(self, events: list[pygame.event.Event], map: list[list[int]], tilewidth: int, tileheight: int, numrows: int, numcolumns: int) -> None:
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_LEFT:
                if self.x - 1 >= 0 and map[self.y][self.x-1] != 1:
                    self.x -= 1
            if event.key == pygame.K_RIGHT:
                if self.x + 1 < numcolumns and map[self.y][self.x+1] != 1:
                    self.x += 1
            if event.key == pygame.K_UP:
                if self.y - 1 >= 0 and map[self.y-1][self.x] != 1:
                    self.y -= 1
            if event.key == pygame.K_DOWN:
                if self.y + 1 < numrows and map[self.y+1][self.x] != 1:
                    self.y += 1
        
        self.x = max(0, min(self.x, numcolumns - 1))
        self.y = max(0, min(self.y, numrows - 1))

