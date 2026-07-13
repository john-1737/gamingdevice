import pygame as pg
from pygame.locals import *
from controller_mac import Controller
pg.font.init()
font = pg.font.SysFont(None, 24)
render_text = lambda text, pos: screen.blit(font.render(text, True, 'white'), pos)
screen = pg.display.set_mode((150, 75))
pg.joystick.init()
controller = Controller()
while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            exit()
    screen.fill('black')
    render_text(f'Left: {controller.get_joystick_value(0, 0)}, {controller.get_joystick_value(0, 1)}', (0, 0))
    render_text(f'Right: {controller.get_joystick_value(1, 0)}, {controller.get_joystick_value(1, 1)}', (0, 25))
    render_text(f"{'[1]' if controller.button_pressed(0) else ' 1 '} \
{'[2]' if controller.button_pressed(1) else ' 2 '} \
{'[3]' if controller.button_pressed(2) else ' 3 '} \
{'[4]' if controller.button_pressed(3) else ' 4 '} \
{'[L]' if controller.button_pressed(4) else ' L '} \
{'[R]' if controller.button_pressed(5) else ' R '}", (0, 50))
    pg.display.update()