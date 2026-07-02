import pygame as pg
from pygame.locals import *
from os import listdir
from joystick import get_joystick_value, button_pressed

screen = pg.display.set_mode((400, 400))
width = 400
pg.display.set_caption('Gaming Device Home Screen')
modules = ['joystick.py', 'homescreen.py', 'keyboard.py', 'num_keyboard.py', 'help.py']
apps = []
for i in listdir():
    if i.endswith('.py') and i not in modules:
        filename = i[:-3]
        exec(f'import {filename}')
        try:
            name = eval(f'{filename}.name')
        except:
            name = filename
        try:
            image = eval(f'{filename}.image')
        except:
            image = 'placeholder.png'
        try:
            help = eval(f'{filename}.help')
        except:
            help = 'A help file has not been\nprovided for this app.'
        apps.append((name, image, filename, help))
pages = len(apps) // 16
pg.font.init()
font = pg.font.SysFont('verdana', int(width/24))
largefont = pg.font.SysFont('verdana', int(width/7))
smallfont = pg.font.SysFont('verdana', int(width/14))


#Remove next 2 functions after getting hardware joystick
# def get_joystick_value(joystick, axis):
#     for event in events:
#         if event.type == JOYAXISMOTION and event.axis == joystick*2+axis:
#             return event.value*100
#     return 0

# def button_pressed(button):
#     for event in events:
#         if event.type == JOYBUTTONDOWN and event.button == (3, 2, 1, 0, 7, 8)[button]:
#             return True
#     return False

def render_text(text, pos, center=False, color=(255, 255, 255), font=font):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect()
    if center:
        width = rect.width/2
        height = rect.height/2
        screen.blit(text_surface, (pos[0]-width,  pos[1]-height))
    else:
        screen.blit(text_surface, pos)

def show_help(text, title='Help'):
    global events
    page = 0
    helptext = text.splitlines()
    helptext = [helptext[i:i + 8] for i in range(0, len(helptext), 8)]
    darkmode = eval(read_settings(1))
    while True:
        events = pg.event.get()
        for event in events:
            if event.type == QUIT:
                pg.quit()
                exit()
            elif event.type == JOYAXISMOTION:
                if abs(round(event.value, 2)) == 1:
                    if event.axis == 0:
                        if event.value <= 0: 
                            page -= 1
                        else:
                            page += 1
        if button_pressed(4):
            return True
        elif button_pressed(1):
            return False
        page %= len(helptext)
        screen.fill((255-darkmode*255,)*3)
        render_text(title, (0, 0), font=largefont, color=(darkmode*255,)*3)
        for i, j in enumerate(helptext[page], start=2):
            render_text(j, (0, width/12 * i), font=smallfont, color=(darkmode*255,)*3)
        render_text('Use left joystick to navigate.', (0, width/12*10), font=smallfont, color=(darkmode*255,)*3)
        render_text('Press left joystick to exit.', (0, width/12*11), font=smallfont, color=(darkmode*255,)*3)
        pg.display.update()

def help_menu():
    global events
    import help
    help_pages = help.help
    help_titles = help.help_titles + ['Back']
    selected = 0
    while True:
        events = pg.event.get()
        for event in events:
            if event.type == QUIT:
                pg.quit()
                exit()
            elif event.type == JOYAXISMOTION:
                if abs(round(event.value, 2)) == 1:
                    if event.axis == 1:
                        if event.value <= 0:
                            selected -= 1
                        else:
                            selected += 1
        if button_pressed(1):
            return
        elif button_pressed(4):
            if help_titles[selected] == 'Back' or not show_help(help_pages[selected][1], help_pages[selected][0]):
                return
        selected %= len(help_pages) + 1
        darkmode = eval(read_settings(1))
        screen.fill((255-darkmode*255,)*3)
        render_text('Help', (0, 0), font=largefont, color=(darkmode*255,)*3)
        for i, j in enumerate(help_titles, start=2):
            render_text(j, (0, width/12 * i), font=smallfont, color=(darkmode*255,)*3)
        pg.draw.rect(screen, ((0, 0, 255), (255, 255, 0))[darkmode], pg.Rect(0, width/12*(selected+2), width, width/12), 2)
        render_text('Use left joystick to navigate.', (0, width/12*10), font=smallfont, color=(darkmode*255,)*3)
        render_text('Press square to exit.', (0, width/12*11), font=smallfont, color=(darkmode*255,)*3)
        pg.display.update()

def show_settings(selected=0):
    options = ('Wallpaper', 'Dark Mode', 'Editor Mode', 'Back')
    images = ("'wallpaper.png'", "'check.png' if darkmode else 'check-empty.png'", "'editormode.png'", "'back.png'")
    commands = (configure_wallpaper, toggle_darkmode, editor_mode)
    while True:
        events = pg.event.get()
        for event in events:
            if event.type == QUIT:
                pg.quit()
                exit()
        if event.axis == 1:
            if event.value <= 0:
                selected -= 1
            else:
                selected += 1
        if button_pressed(1):
            return
        elif button_pressed(4):
            if options[selected] == 'Back' or commands[selected]():
                return
        selected %= len(options)
        darkmode = eval(read_settings(1))
        screen.fill((255-darkmode*255,)*3)
        render_text('Settings', (0, 0), font=largefont, color=(darkmode*255,)*3)
        for i, j in enumerate(zip(options, images), start=2):
            render_text(j[0], (width/12, width/12 * i), font=smallfont, color=(darkmode*255,)*3)
            screen.blit(pg.transform.scale(pg.image.load(eval(j[1])).convert_alpha(), (width/12, width/12)), (0, width/12 * i))
        pg.draw.rect(screen, ((0, 0, 255), (255, 255, 0))[darkmode], pg.Rect(0, width/12*(selected+2), width, width/12), 2)
        render_text('Use left joystick to navigate.', (0, width/12*10), font=smallfont, color=(darkmode*255,)*3)
        render_text('Press square to exit.', (0, width/12*11), font=smallfont, color=(darkmode*255,)*3)
        pg.display.update()

def toggle_darkmode():
    darkmode = eval(read_settings(1))
    darkmode = not darkmode
    write_settings(1, str(darkmode))
    return True

def editor_mode():
    darkmode = eval(read_settings(1))
    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pg.quit()
                    exit()
        if button_pressed(4):
            return True
        elif button_pressed(1):
            return False
        screen.fill((255-darkmode*255,)*3)
        render_text('Editor Mode', (0, 0), font=largefont, color=(darkmode*255,)*3)
        for i, j in enumerate('''To enter editor mode, follow
these steps:
• Connect a keyboard to the
device.
• Press ESC on the
keyboard.
For more details, see the
help page for Editor Mode.'''.splitlines(), start=2):
            render_text(j, (0, width/12 * i), font=smallfont, color=(darkmode*255,)*3)
        render_text('Press left joystick to exit.', (0, width/12*11), font=smallfont, color=(darkmode*255,)*3)
        pg.display.update()

def write_settings(line, text):
    with open('stats.txt', 'r') as f:
        file = f.read().splitlines()
    file[line] = text
    with open('stats.txt', 'w') as f:
        f.write('\n'.join(file))

def read_settings(line):
    with open('stats.txt') as f:
        return f.read().splitlines()[line]

def configure_wallpaper():
    selected = 0
    options = ('National Park', 'Moon Viewing', 'Back')
    images = ('nationalpark.png', 'moonviewing.png', 'back.png')
    darkmode = eval(read_settings(1))
    events = pg.event.get()
    while True:
        for event in events:
            if event.type == QUIT:
                pg.quit()
                exit()
            elif event.type == JOYAXISMOTION:
                if abs(round(event.value, 2)) == 1:
                    if event.axis == 1:
                        if event.value <= 0:
                            selected -= 1
                        else:
                            selected += 1
        if button_pressed(1):
            return False
        elif button_pressed(4):
            if options[selected] != 'Back':
                write_settings(0, images[selected])
            return True
        selected %= len(options)
        screen.fill((255-darkmode*255,)*3)
        render_text('Wallpaper', (0, 0), font=largefont, color=(darkmode*255,)*3)
        for i, j in enumerate(zip(options, images), start=2):
            render_text(j[0], (width/12, width/12 * i), font=smallfont, color=(darkmode*255,)*3)
            screen.blit(pg.transform.scale(pg.image.load(j[1]).convert_alpha(), (width/12, width/12)), (0, width/12 * i))
        pg.draw.rect(screen, ((0, 0, 255), (255, 255, 0))[darkmode], pg.Rect(0, width/12*(selected+2), width, width/12), 2)
        render_text('Use left joystick to navigate.', (0, width/12*10), font=smallfont, color=(darkmode*255,)*3)
        render_text('Press square to exit.', (0, width/12*11), font=smallfont, color=(darkmode*255,)*3)
        pg.display.update()

cursor = 0
page = 0
pg.joystick.init()
joystick = pg.joystick.Joystick(0)
while True:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        elif event.type == JOYAXISMOTION:
            if abs(round(event.value, 2)) == 1:
                if event.axis == 0:
                    if event.value >= 0:
                        if cursor != len(apps) - 1:
                            cursor += 1
                    else:
                        if cursor != 0:
                            cursor -= 1
                elif event.axis == 1:
                    if event.value >= 0:
                        if cursor + 4 <= len(apps) - 1:
                            cursor += 4
                    else:
                        if cursor - 4 >= 0:
                            cursor -= 4
                elif event.axis == 2:
                    if event.value >= 0:
                        if page != pages:
                            cursor += 16
                    else:
                        if page != 0:
                            cursor -= 16
    if button_pressed(4):
        exec(f'{apps[cursor][2]}.play(screen)')
    elif button_pressed(2):
        show_help(apps[cursor][3])
    elif button_pressed(0):
        show_settings()
    elif button_pressed(1):
        help_menu()
    page = cursor // 16
    if cursor >= len(apps):
        cursor = len(apps) - 1
    wallpaper = read_settings(0)
    screen.fill((0, 0, 0))
    screen.blit(pg.transform.scale(pg.image.load(wallpaper).convert_alpha(), (width, width)), (0, 0))
    for i, j in enumerate(apps[page*16:]):
        screen.blit(pg.transform.scale(pg.image.load(j[1]).convert_alpha(), (width/20*4, width/20*4)), ((i%4)*width/4+width/40, (i//4)*width/4))
        if font.render(j[0], True, (255, 255, 255)).get_rect().width <= width/4:
            render_text(j[0], ((i%4)*width/4+width/8, (i//4)*width/4+width/40*9), center=True)
        else:
            for k in range(2, len(j[0])+4):
                if font.render((j[0][:k])+'...', True, (255, 255, 255)).get_rect().width > width/4:
                    render_text((j[0][:k-1])+'...', ((i%4)*width/4+width/8, (i//4)*width/4+width/40*9), center=True)
                    break
    pg.draw.rect(screen, (255, 255, 255), pg.Rect(((cursor-16*page)%4)*width/4, ((cursor-16*page)//4)*width/4, width/4, width/4), 2)
    pg.display.update()