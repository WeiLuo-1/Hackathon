import pygame
import sys
import maze
import constants
import random
pygame.init()
win = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
clock = pygame.time.Clock()
def main():
    # 设置屏幕宽度和高度
  
    create_maze()

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_maze()

    pygame.quit()
    print_maze(maze)
    sys.exit()


if __name__ == "__main__":
    main()
