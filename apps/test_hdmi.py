import os
import pygame as pg

pg.init()

screen = pg.display.set_mode((400, 400))
width = 400

image = pg.image.load('desert.png').convert_alpha()
image = pg.transform.scale(image, (width, width))

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

    screen.fill((0, 0, 0))
    screen.blit(image, (0, 0))
    pg.display.flip()
