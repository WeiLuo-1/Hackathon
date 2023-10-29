import pygame

def level(lvl):
    ROWS, COLS = lvl + 8, 8 + lvl
    if ROWS >=  38 or COLS >=38:
        ROWS = 38
        COLS = 38
    return ROWS, COLS
    
