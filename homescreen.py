#Homescreen, written originally for Pi, now modified on Mac
import pygame as pg
from pygame.locals import *
from os import listdir
from time import sleep, localtime
pg.init()
try:
    from controller_mac import Controller
    screen = pg.display.set_mode((300, 300))
except ModuleNotFoundError:
    from controller_pi import Controller
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    from os import chdir
    chdir('/home/gaming/gamingdevice')
from keyboard import keyboard

controller = Controller() #Create a Controller object.
get_joystick_value, button_pressed = controller.get_joystick_value, controller.button_pressed

width = screen.get_width()
pg.display.set_caption('Gaming Device Home Screen')
pg.mouse.set_visible(False)
modules = ['joystick.py', 'homescreen.py', 'help.py', 'joystick.py', 'code.py', 'num_keyboard.py', 'num_keyboard2.py', 'keyboard.py', 'buttons.py', 'controller_mac.py',\
           'controller_pi.py', 'test.py', 'test2.py']
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
font = pg.font.Font('Verdana.ttf', int(width/24))
largefont = pg.font.Font('Verdana.ttf', int(width/7))
smallfont = pg.font.Font('Verdana.ttf', int(width/14))
tfont = pg.font.Font('Verdana.ttf', int(width/9))

def render_text(text, pos, center=False, color=(255, 255, 255), font=font, image=None):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect()
    if center:
        width = rect.width/2
        height = rect.height/2
        screen.blit(text_surface, (pos[0]-width,  pos[1]-height))
    else:
        if image == None:
            screen.blit(text_surface, pos)
        else:
            screen.blit(text_surface, (pos[0]+(image.get_rect().width), pos[1]))
            screen.blit(image, pos)

def editor_mode():
    darkmode = eval(read_settings(1))
    sleep(0.2)
    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pg.quit()
                    exit()
        if button_pressed(1):
            return False
        elif button_pressed(4):
            return True
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

def show_search():
    search_apps = sorted(apps, key=lambda x: x[0])
    lightlabels = eval(read_settings(2))
    darkmode = eval(read_settings(1))
    search_criteria = ''
    search_pages = len(search_apps) // 7 + 1
    search_page = 0
    selected = 0
    sleep(0.2)
    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
        if button_pressed(1):
            sleep(0.2)
            return
        elif button_pressed(4):
            if selected == 0:
                sleep(0.2)
                search_criteria = keyboard(screen, controller, search_criteria, 'Type to search', darkmode=darkmode)
                search_criteria = '' if search_criteria == None else search_criteria
            else:
                exec(f'{search_apps[selected-1][2]}.play(screen, controller)')
                sleep(0.2)
                return
        val = get_joystick_value(0, 1)
        if abs(val) > 75:
            if val <= 0:
                selected += 1
                sleep(0.2)
            else:
                selected -= 1
                sleep(0.2)
        val = get_joystick_value(1, 0)
        if val < -75:
            return
        search_apps = [i for i in sorted(apps, key=lambda x: x[0]) if search_criteria.lower() in i[0].lower()]
        selected %= len(search_apps) + 1
        if selected == 0:
            search_page = 0
        else:
            search_page = (selected-1)//7*7
        wallpaper = read_settings(0)
        screen.fill((0, 0, 0))
        screen.blit(pg.transform.scale(pg.image.load(wallpaper).convert_alpha(), (width, width)), (0, 0))
        render_text('Search', (0, 0), font=largefont, color=(lightlabels*255,)*3)
        if search_criteria:
            render_text(search_criteria, (width/12, width/6), font=smallfont, color=(lightlabels*255,)*3)
        else:
            render_text('Type to search', (width/12, width/6), font=smallfont, color=(100, 100, 100))
        screen.blit(pg.transform.scale(pg.image.load('magnifier.png').convert_alpha(), (width/12, width/12)), (0, width/6))
        for i, j in enumerate(search_apps[search_page:search_page+7], start=3):
            render_text(j[0], (width/12, width/12 * i), font=smallfont, color=(lightlabels*255,)*3)
            screen.blit(pg.transform.scale(pg.image.load(j[1]).convert_alpha(), (width/12, width/12)), (0, width/12 * i))
        if selected == 0:
            pg.draw.rect(screen, ((0, 0, 255), (255, 255, 0))[lightlabels], pg.Rect(0, width/12*2, width, width/12), 2)
        else:
            pg.draw.rect(screen, ((0, 0, 255), (255, 255, 0))[lightlabels], pg.Rect(0, width/12*(((selected-1)%7)+3), width, width/12), 2)
        render_text('Use left joystick to navigate.', (0, width/12*10), font=smallfont, color=(lightlabels*255,)*3)
        render_text('Press square to exit.', (0, width/12*11), font=smallfont, color=(lightlabels*255,)*3)
        pg.display.update()

def show_help(text, title='Help'):
    page = 0
    triangle = pg.transform.scale(pg.image.load('triangle.png').convert_alpha(), (width/12, width/12))
    circle = pg.transform.scale(pg.image.load('circle.png').convert_alpha(), (width/12, width/12))
    square = pg.transform.scale(pg.image.load('square.png').convert_alpha(), (width/12, width/12))
    cross = pg.transform.scale(pg.image.load('cross.png').convert_alpha(), (width/12, width/12))
    warning = pg.transform.scale(pg.image.load('warning.png').convert_alpha(), (width/12, width/12))
    helptext = text.splitlines()
    showpage = eval(read_settings(3))
    pagelength = 7 if len(helptext) > 8 and showpage else 8
    helptext = [helptext[i:i + pagelength] for i in range(0, len(helptext), pagelength)]
    darkmode = eval(read_settings(1))
    sleep(0.2)
    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
        if button_pressed(1):
            return False
        elif button_pressed(4):
            return True
        val = get_joystick_value(0, 0)
        if abs(val) > 75:
            if val <= 0:
                page -= 1
                sleep(0.2)
            else:
                page += 1
                sleep(0.2)
        page %= len(helptext)
        screen.fill((255-darkmode*255,)*3)
        render_text(title, (0, 0), font=largefont, color=(darkmode*255,)*3)
        for i, j in enumerate(helptext[page], start=2):
            for k, l in zip(('{square}', '{triangle}', '{circle}', '{cross}', '{warning}', ''), (square, triangle, circle, cross, warning, None)):
                if j.startswith(k):
                    render_text(j[len(k):], (0, width/12 * i), font=smallfont, color=(darkmode*255,)*3, image=l)
                    break
        pg.draw.line(screen, (darkmode*255,)*3, (0, width/12*10), (width, width/12*10), width=1)
        if len(helptext) != 1 and showpage:
            pg.draw.line(screen, (darkmode*255,)*3, (0, width/12*9), (width, width/12*9), width=1)
            render_text(f'Page {page+1} of {len(helptext)}', (0, width/12*9), font=smallfont, color=(darkmode*255,)*3)
        render_text('Use left joystick to navigate.', (0, width/12*10), font=smallfont, color=(darkmode*255,)*3)
        render_text('Press left joystick to exit.', (0, width/12*11), font=smallfont, color=(darkmode*255,)*3)
        pg.display.update()

def help_menu():
    import help
    help_pages = help.help
    help_titles = help.help_titles + ['Back']

    selected = 0
    sleep(0.2)
    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
        if button_pressed(1):
            return
        elif button_pressed(4):
            if help_titles[selected] == 'Back' or not show_help(help_pages[selected][1], help_pages[selected][0]):
                return
            sleep(0.2)
        val = get_joystick_value(0, 1)
        if abs(val) > 75:
            if val <= 0:
                selected += 1
                sleep(0.2)
            else:
                selected -= 1
                sleep(0.2)
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
    options = ('Wallpaper', 'Dark Mode', 'Light Home Screen Labels', 'Show Help Page Number', 'Show Home Screen Info', 'Editor Mode', 'Back')
    images = ("'wallpaper.png'", "'check.png' if darkmode else 'check-empty.png'", "'check.png' if lightlabels else 'check-empty.png'", "'check.png' if showpage else 'check-empty.png'",\
              "'check.png' if showinfo else 'check-empty.png'", "'editormode.png'", "'back.png'")
    commands = (configure_wallpaper, toggle_darkmode, toggle_lightlabels, toggle_showpage, toggle_showinfo, editor_mode)
    sleep(0.2)
    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
        if button_pressed(1):
            return
        elif button_pressed(4):
            if options[selected] == 'Back' or not commands[selected]():
                return
            sleep(0.2)
        val = get_joystick_value(0, 1)
        if abs(val) > 75:
            if val <= 0:
                selected += 1
                sleep(0.2)
            else:
                selected -= 1
                sleep(0.2)
        selected %= len(options)
        darkmode = eval(read_settings(1))
        lightlabels = eval(read_settings(2))
        showpage = eval(read_settings(3))
        showinfo = eval(read_settings(4))
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

def toggle_lightlabels():
    lightlabels = eval(read_settings(2))
    lightlabels = not lightlabels
    write_settings(2, str(lightlabels))
    return True

def toggle_showpage():
    showpage = eval(read_settings(3))
    showpage = not showpage
    write_settings(3, str(showpage))
    return True

def toggle_showinfo():
    showinfo = eval(read_settings(4))
    showinfo = not showinfo
    write_settings(4, str(showinfo))
    return True

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
    options = sorted(('National Park', 'Moon Viewing Ceremony', 'Desert', 'Clouds', 'Bridge with Clouds', 'Bridge at Night', 'Lake at Sunrise')) + ['Back']
    images = sorted(('nationalpark.png', 'moonviewing.png', 'desert.png', 'clouds.png', 'bridge-with-clouds.png', 'bridge-night.png', 'lake-sunrise.png')) + ['back.png']
    darkmode = eval(read_settings(1))
    sleep(0.2)
    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
        if button_pressed(1):
            return
        elif button_pressed(4):
            if options[selected] != 'Back':
                write_settings(0, images[selected])
            return True
        val = get_joystick_value(0, 1)
        if abs(val) > 75:
            if val <= 0:
                selected += 1
                sleep(0.2)
            else:
                selected -= 1
                sleep(0.2)
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

showinfo = eval(read_settings(4))
cursor = 2*showinfo
page = 0
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
    val = get_joystick_value(0, 0)
    if abs(val) > 75:
        if val >= 0:
            if cursor != len(apps) + 2*showinfo - 1:
                cursor += 1
                sleep(0.2)
        else:
            if cursor != 0:
                cursor -= 1
                sleep(0.2)
    val = get_joystick_value(0, 1)
    if abs(val) > 75:
        if val <= 0:
            if cursor + 4 <= len(apps) + 2*showinfo - 1:
                cursor += 4
                sleep(0.2)
        else:
            if cursor - 4 >= 0:
                cursor -= 4
                sleep(0.2)
    val = get_joystick_value(1, 0)
    if abs(val) > 75:
        if val >= 0:
            if page != pages:
                cursor += 16
                sleep(0.2)
            else:
                show_search()
                sleep(0.2)
        else:
            if page != 0:
                cursor -= 16
                sleep(0.2)
    if button_pressed(4):
        exec(f'{([apps[0]] * 2 * showinfo + apps)[cursor][2]}.play(screen, controller)')
        sleep(0.2)
    elif button_pressed(2):
        show_help(([apps[0]] * 2 * showinfo + apps)[cursor][3])
        sleep(0.2)
    elif button_pressed(0):
        show_settings()
        sleep(0.2)
    elif button_pressed(1):
        help_menu()
        sleep(0.2)
    elif button_pressed(3):
        show_search()
        sleep(0.2)
    page = cursor // 16
    showinfo = eval(read_settings(4))
    if cursor >= len(apps) + 2*showinfo:
        cursor = len(apps) + 2*showinfo - 1
    if cursor < 2 and showinfo:
        cursor = 2
    wallpaper = read_settings(0)
    lightlabels = eval(read_settings(2))
    screen.fill((0, 0, 0))
    screen.blit(pg.transform.scale(pg.image.load(wallpaper).convert_alpha(), (width, width)), (0, 0))
    for i, j in enumerate(([('', 'blank.png', apps[0][2], apps[0][3])] * 2 * showinfo + apps)[page*16:]):
        screen.blit(pg.transform.scale(pg.image.load(j[1]).convert_alpha(), (width/20*4, width/20*4)), ((i%4)*width/4+width/40, (i//4)*width/4))
        if font.render(j[0], True, (255, 255, 255)).get_rect().width <= width/4:
            render_text(j[0], ((i%4)*width/4+width/8, (i//4)*width/4+width/40*9), center=True, color=(lightlabels*255,)*3)
        else:
            for k in range(2, len(j[0])+4):
                if font.render((j[0][:k])+'...', True, (255, 255, 255)).get_rect().width > width/4:
                    render_text((j[0][:k-1])+'...', ((i%4)*width/4+width/8, (i//4)*width/4+width/40*9), center=True, color=(lightlabels*255,)*3)
                    break
    pg.draw.rect(screen, ((0, 0, 255), (255, 255, 0))[lightlabels], pg.Rect(((cursor-16*page)%4)*width/4, ((cursor-16*page)//4)*width/4, width/4, width/4), 2)
    t = localtime()
    if showinfo and page == 0: 
        render_text(f'{t.tm_hour%12}:{str(t.tm_min).zfill(2)}', (0, 0), font=tfont, color=(lightlabels*255,)*3)
    pg.display.update()