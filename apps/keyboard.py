import pygame as pg
from pygame.locals import *

keyboards = ('abcdefghijklmnopqrstuvwxyz',
'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 
'1234567890?!.,@#$%^&*()/\'"',
'1234567890{}[]+-=_|\\:;<>~`')

def keyboard(s, starttext='', inittext=''):
    global screen, font, width, smallfont
    screen = s
    pg.joystick.init()
    joystick = pg.joystick.Joystick(0)
    width = screen.get_width()
    help = pg.transform.scale(pg.image.load('help.png').convert_alpha(), (width/6, width/6))
    clear = pg.transform.scale(pg.image.load('clear.png').convert_alpha(), (width/6, width/6))
    font = pg.font.SysFont('verdana', int(width/7))
    smallfont = pg.font.SysFont('verdana', int(width/14))
    text_cursor = len(starttext)
    current_kb = 0
    cursor = 1
    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            elif event.type == JOYBUTTONDOWN:
                if event.button == 2:
                    return None
                elif event.button == 0 and starttext != '':
                        starttext = list(starttext)
                        del starttext[text_cursor-1]
                        starttext = ''.join(starttext)
                        text_cursor -= 1
                elif event.button == 7:
                    if cursor in range(1, 27):
                        starttext = list(starttext)
                        starttext.insert(text_cursor, (' '+keyboards[current_kb])[cursor])
                        starttext = ''.join(starttext)
                        text_cursor += 1
                    elif cursor == 28:
                        starttext = list(starttext)
                        starttext.insert(text_cursor, ' ')
                        starttext = ''.join(starttext)
                        text_cursor += 1
                    elif cursor == 27:
                        if not show_help():
                            return None
                    elif cursor == 0:
                        clear_cursor = 1
                        clearing = True
                        while clearing:
                            for event in pg.event.get():
                                if event.type == QUIT:
                                    pg.quit()
                                    exit()
                                elif event.type == JOYBUTTONDOWN:
                                    if event.button == 2:
                                        return None
                                    elif event.button == 7:
                                        if not clear_cursor:
                                            starttext = ''
                                            text_cursor = 0
                                        clearing = False
                                elif event.type == JOYAXISMOTION:
                                    if abs(round(event.value, 2)) == 1:
                                        if event.axis == 1:
                                            if event.value >= 0:
                                                if clear_cursor != 1:
                                                    clear_cursor += 1
                                            else:
                                                if clear_cursor != 0:
                                                    clear_cursor -= 1
                            screen.fill((0, 0, 0))
                            render_text('Clear all?', (0, 0), font=font)
                            render_text('Yes', (0, width/6), font=font)
                            render_text('No', (0, width/3), font=font)
                            pg.draw.rect(screen, (255, 255, 0), pg.Rect(0, width/6*(clear_cursor+1), width, width/6), 2)
                            pg.display.update()
                elif event.button == 8:
                    return starttext
                elif event.button == 1:
                    if current_kb in (0, 1):
                        current_kb = 2
                    else:
                        current_kb = 0
                elif event.button == 3:
                    if current_kb in (0, 2):
                        current_kb += 1
                    else:
                        current_kb -= 1
            elif event.type == JOYAXISMOTION:
                if abs(round(event.value, 2)) == 1:
                    if event.axis == 0:
                        if event.value <= 0: 
                            if cursor != 0:
                                cursor -= 1
                        elif cursor != 28:
                            cursor += 1        
                    elif event.axis == 1:
                        if event.value <= 0:
                            if cursor != 0:
                                cursor -= 6
                                if cursor < 0:
                                    cursor = 0
                        elif cursor < 25:
                            cursor += 6
                            if cursor > 28:
                                cursor = 28
                    elif event.axis == 2:
                        if event.value <= 0: 
                            if text_cursor != 0:
                                text_cursor -= 1
                        elif text_cursor != len(starttext):
                            text_cursor += 1        
                    elif event.axis == 3:
                        if event.value <= 0:
                            text_cursor = 0
                        else:
                            text_cursor = len(starttext)
        screen.fill((0,0,0))
        if cursor == 28:
            pg.draw.rect(screen, (255, 255, 0), pg.Rect(width/2, width/6*5, width/2, width/6), 2)
        else:
            pg.draw.rect(screen, (255, 255, 0), pg.Rect(((cursor+5)%6)*width/6, ((cursor+5)//6)*width/6, width/6, width/6), 2)
        for i, j in enumerate(keyboards[current_kb]):
            render_text(j, (((i+6)%6)*width/6+width/12, ((i+6)//6)*width/6+width/12), center=True, font=font)
        render_text('space', (width/12*9, width/12*11), center=True, font=font)
        textwidth = font.render(starttext[:text_cursor], True, (255, 255, 255)).get_rect().width + font.render('|', True, (255, 255, 255)).get_rect().width
        spacewidth = font.render(starttext[text_cursor:], True, (255, 255, 255)).get_rect().width
        if starttext == '':
            render_text(inittext, (0, 0), font=font, color=(128, 128, 128))
        elif textwidth+spacewidth <= width/6*5:
            render_text(starttext[:text_cursor], (0, 0), font=font)
            render_text('|', (textwidth-font.render('|', True, (255, 255, 255)).get_rect().width, 0), font=font, color=(0, 0, 255))
            render_text(starttext[text_cursor:], (textwidth, 0), font=font)
        else:
            render_text(starttext[:text_cursor], (width/6*5-font.render('|', True, (255, 255, 255)).get_rect().width, 0), font=font, lanchor=True)
            render_text('|', (width/6*5, 0), font=font, lanchor=True, color=(0, 0, 255))
        screen.blit(help, (width/6*2, width/6*5))
        screen.blit(clear, (width/6*5, 0))
        pg.display.update()
pg.font.init()

def render_text(text, pos, font, center=False, lanchor=False, color=(255, 255, 255)):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect()
    if center:
        width = rect.width/2
        height = rect.height/2
        screen.blit(text_surface, (pos[0]-width,  pos[1]-height))
    elif lanchor:
        width = rect.width
        screen.blit(text_surface, (pos[0]-width,  pos[1]))
    else:
        screen.blit(text_surface, pos)

def show_help():
    page = 0
    helptext = ['''Left joystick movement:
keyboard cursor
Right joystick movement:
text cursor
Left joystick press:
select key
Right joystick press:
close keyboard'''.splitlines(),
'''Cross button: backspace
Triangle button: caps lock
Circle button: number lock
Square button: exit app



'''.splitlines()]
    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            elif event.type == JOYBUTTONDOWN:
                if event.button == 2:
                    return False
                elif event.button == 7:
                    return True
            elif event.type == JOYAXISMOTION:
                if abs(round(event.value, 2)) == 1:
                    if event.axis == 0:
                        if event.value <= 0: 
                            page += 1
                        else:
                            page -= 1
        page %= len(helptext)
        screen.fill((0, 0, 0))
        render_text('Help', (0, 0), font=font)
        for i, j in enumerate(helptext[page], start=2):
            render_text(j, (0, width/12 * i), font=smallfont)
        render_text('Use left joystick to navigate.', (0, width/12*10), font=smallfont)
        render_text('Press left joystick to exit.', (0, width/12*11), font=smallfont)
        pg.display.update()

if __name__ == '__main__':
    keyboard(pg.display.set_mode((300, 300)), inittext='Enter text')