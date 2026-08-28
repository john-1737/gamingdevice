import pygame as pg
from pygame.locals import *

def play(s):
    global screen
    screen = s
    width = screen.get_width()
    rocket = pg.transform.scale(pg.image.load('rocket.png').convert_alpha(), (width/5, width/5))
    ufo = pg.transform.scale(pg.image.load('ufo.png').convert_alpha(), (width/5, width/5))
    comet = pg.transform.scale(pg.image.load('comet.png').convert_alpha(), (width/5, width/5))
    pg.init()
    pg.font.init()
    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            screen.fill((0, 0, 0))
            screen.blit(rocket, (width/5*2, width/5*4))
            pg.display.update()

if __name__ == '__main__':
    play(pg.display.set_mode((400, 400)))