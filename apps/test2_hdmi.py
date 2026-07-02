import os
os.environ["SDL_VIDEODRIVER"] = "kmsdrm"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame as pg

pg.init()
screen = pg.display.set_mode((640, 480))
screen.fill((0, 0, 255))
pg.display.flip()

while True:
    pass