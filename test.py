import pygame as pg
from pygame.locals import *
pg.font.init()
font = pg.font.SysFont(None, 24)
render_text = lambda text, pos: screen.blit(font.render(text, True, 'white'), pos)
screen = pg.display.set_mode((150, 75))
pg.joystick.init()
joystick = pg.joystick.Joystick(0)
while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            exit()
    screen.fill('black')
    render_text(f'Left: {int(joystick.get_axis(0)*100)}, {int(joystick.get_axis(1)*100)}', (0, 0))
    render_text(f'Right: {int(joystick.get_axis(2)*100)}, {int(joystick.get_axis(3)*100)}', (0, 25))
    render_text(f"{'[1]' if joystick.get_button(3) else ' 1 '} \
{'[2]' if joystick.get_button(2) else ' 2 '} \
{'[3]' if joystick.get_button(1) else ' 3 '} \
{'[4]' if joystick.get_button(0) else ' 4 '} \
{'[L]' if joystick.get_button(7) else ' L '} \
{'[R]' if joystick.get_button(8) else ' R '}", (0, 50))
    pg.display.update()