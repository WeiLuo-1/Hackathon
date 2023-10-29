import pygame
import os
import constants

os.environ['SDL_AUDIODRIVER'] = 'dsp'

class Player:
    def __init__(self, sprite: pygame.Surface) -> None:
        self.x = 0
        self.y = 0
        self.sprite = pygame.image.load(r'\\wsl.localhost\Ubuntu\home\wocqcm\Desktop\Hackathon\cat.png')
    
    def draw(self, window, tilewidth: int, tileheight: int) -> None:
        """
        Draws the player.
        """
        screenx = self.x * tilewidth
        screeny = self.y * tileheight
        self.sprite = pygame.transform.scale(self.sprite, (tilewidth, tileheight))
        window.blit(self.sprite, (screenx, screeny))
    
    def process(self, command: str, map: list[list[int]], tilewidth: int, tileheight: int, numrows: int, numcolumns: int) -> None:

        if command == constants.COMMAND_MOVE_LEFT:
            if self.x - 1 >= 0 and map[self.y][self.x-1] != 1:
                self.x -= 1
        if command == constants.COMMAND_MOVE_RIGHT:
            if self.x + 1 < numcolumns and map[self.y][self.x+1] != 1:
                self.x += 1
        if command == constants.COMMAND_MOVE_UP:
            if self.y - 1 >= 0 and map[self.y-1][self.x] != 1:
                self.y -= 1
        if command == constants.COMMAND_MOVE_DOWN:
            if self.y + 1 < numrows and map[self.y+1][self.x] != 1:
                self.y += 1
        
        self.x = max(0, min(self.x, numcolumns - 1))
        self.y = max(0, min(self.y, numrows - 1))
