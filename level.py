import pygame

def level(lvl):
    ROWS, COLS = lvl*2 + 15,  lvl + 15
    if ROWS >=  38 or COLS >=38:
        ROWS = 38
        COLS = 38
    return ROWS, COLS
    
