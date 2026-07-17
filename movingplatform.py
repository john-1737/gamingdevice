import pygame as pg
from pygame.locals import *
from random import randint, randrange
try:
    from controller_mac import Controller
except ModuleNotFoundError:
    from controller_pi import Controller
from time import sleep

image = 'movingplatform.png'
name = 'Moving Platform'
help = '''Welcome to Moving
Platform!
This is a platform game
where the platforms move
from left to right and you
jump over them. Press the
left joystick to jump across
platforms.'''

def play(s, c):
    global screen
    screen = s
    get_joystick_value, button_pressed = c.get_joystick_value, c.button_pressed
    width = screen.get_width()
    pg.init()
    pg.font.init()
    font = pg.font.SysFont('Arial', int(width/21))
    titlefont = pg.font.SysFont('Arial', int(width/8))

    def render_text(text, pos, color=(0, 0, 0), font=font):
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, pos)

    def get_platform_top(runner_y):
        for i in platforms:
            if width/10*3 >= i[0] and width/10*3 <= i[0] + i[2] and runner_y <= i[1] and runner_y >= i[1] - relativec(4):
                return i[1]
        return None

    def get_platform(runner_y):
        for i in platforms:
            if width/10*3 >= i[0] and width/10*3 <= i[0] + i[2] and runner_y <= i[1] and runner_y >= i[1] - relativec(4):
                return i
        return None

    relativec = lambda distance: distance*width/400

    runner = pg.transform.scale(pg.image.load('runner.png').convert_alpha(), (width/5, width/5))
    sleep(0.2)
    while True:
        start = True
        while start:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
            if button_pressed(1): return
            elif button_pressed(0): #Take the tutorial.
                sleep(0.2)
                tutorial = True
                clock = pg.time.Clock()
                while tutorial:
                    platforms = [[0, width/4*3, width, 'Press the left joystick to jump.', 0],\
                                    [width+width/4, width/4*3, width, 'Try jumping to a platform above you.', 1],\
                                    [width*2+width/4+width/6, width/4*3-width/6, width, 'Now try jumping to one below you.', 2],\
                                    [width*3+width/4+width/3, width/4*3, width*2, 'You\'re ready to play!', 3]]
                    playing = True
                    runner_jump = 0
                    runner_y = width/4*3
                    text = 'Press the left joystick to jump.'
                    num = 0
                    while playing:
                        for event in pg.event.get():
                            if event.type == pg.QUIT:
                                pg.quit()
                                exit()
                        if button_pressed(1): return
                        elif button_pressed(4) and get_platform_top(runner_y) != None:
                            runner_jump = 60
                        elif button_pressed(0):
                            playing = False
                            tutorial = False
                            sleep(0.2)
                        screen.fill((0, 255, 255))
                        for i in platforms[:]:
                            i[0] -= relativec(1)
                            if i[0] <= -i[2]:
                                platforms.remove(i)
                            else:
                                pg.draw.rect(screen, (255, 0, 255), pg.Rect(i[0], i[1], i[2], width/20))
                                pg.draw.rect(screen, (255, 0, 0), pg.Rect(i[0], i[1], i[2], width/20), int(width/100))
                        if runner_jump:
                            runner_y -= relativec(4)
                            runner_jump -= 1
                        elif get_platform_top(runner_y) == None:
                            runner_y += relativec(4)
                            if runner_y >= width+width/5:
                                # platforms = [[0, width/4*3, width, 'Press the left joystick to jump.', 0],\
                                #  [width+width/4, width/4*3, width, 'Try jumping to a platform above you.', 1],\
                                #  [width*2+width/4+width/6, width/4*3-width/6, width, 'Now try jumping to one below you.', 2],\
                                #  [width*3+width/4+width/3, width/4*3, width*2, 'You\'re ready to play!', 3]][num:]
                                # for i in platforms:
                                #     for j, k in enumerate((0, width+width/4, width*2+width/4+width/6, width*3+width/4+width/3)):
                                #         if num == j:
                                #             i[0] -= k
                                playing = False
                        else:
                            runner_y = get_platform_top(runner_y)
                            p = get_platform(runner_y)
                            text = p[3]
                            num = p[4]
                            if int(platforms[-1][0]) <= -width/2:
                                playing = False
                                tutorial = False
                        screen.blit(runner, (width/5, runner_y-width/5))
                        render_text(text, (0, 0))
                        render_text(f'{num}/3 complete', (0, width/20))
                        render_text('You\'re in the tutorial. Press the triangle to exit.', (0, width/10))
                        pg.display.update()
                        clock.tick(100)
            elif button_pressed(4):
                start = False
                sleep(0.2)
            screen.fill((0, 255, 255))
            pg.draw.rect(screen, (255, 0, 255), pg.Rect(0, width/4*3, width, width/20))
            pg.draw.rect(screen, (255, 0, 0), pg.Rect(-width/100, width/4*3, width+width/50, width/20), int(width/100))
            screen.blit(runner, (width/5, width/4*3-width/5))
            render_text('Moving Platform', (0, 0), font=titlefont)
            render_text('Press left joystick to start the game.', (0, width/5-width/20))
            render_text('Press triangle to take the tutorial.', (0, width/5))
            pg.display.update()
        playing = True
        runner_y = width/4*3
        runner_jump = 0
        platforms = [[0, width/4*3, width, width/4, True, False]]
        clock = pg.time.Clock()
        timer = 0
        score = 0
        while playing:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
            if button_pressed(1): return
            elif button_pressed(4) and get_platform_top(runner_y) != None:
                runner_jump = 60
            screen.fill((0, 255, 255))
            for i in platforms[:]:
                i[0] -= relativec(1)
                if i[0] <= -i[2]:
                    platforms.remove(i)
                else:
                    pg.draw.rect(screen, (255, 0, 255), pg.Rect(i[0], i[1], i[2], width/20))
                    pg.draw.rect(screen, (255, 0, 0), pg.Rect(i[0], i[1], i[2], width/20), int(width/100))
                    if i[0] + i[3] + i[2] <= width and i[4]:
                        i[4] = False
                        platforms.append([width, width/4*3+randint(int(-relativec(timer/8)), int(relativec(timer/8+1))), randint(int(0)+1, int(relativec(timer))+1), width/randint(1, timer+1), True, \
                        False])
            if runner_jump:
                runner_y -= relativec(4)
                runner_jump -= 1
            elif get_platform_top(runner_y) == None:
                runner_y += relativec(4)
                if runner_y >= width+width/5:
                    playing = False
            else:
                runner_y = get_platform_top(runner_y)
                p = get_platform(runner_y)
                if p[5] == False:
                    p[5] = True
                    score += 1
            screen.blit(runner, (width/5, runner_y-width/5))
            render_text(f'Score: {score}', (0, 0))
            pg.display.update()
            clock.tick(100)
            timer += 1
        end = True
        while end:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
            if button_pressed(1): return
            elif button_pressed(4):
                end = False
                sleep(0.2)
            screen.fill((0, 255, 255))
            for i in platforms[:]:
                if i[0] <= -i[2]:
                    platforms.remove(i)
                else:
                    pg.draw.rect(screen, (255, 0, 255), pg.Rect(i[0], i[1], i[2], width/20))
                    pg.draw.rect(screen, (255, 0, 0), pg.Rect(i[0], i[1], i[2], width/20), int(width/100))
                    if i[0] + i[3] + i[2] <= width and i[4]:
                        i[4] = False
                        platforms.append([width, width/4*3+randint(int(-relativec(timer/8)), int(relativec(timer/8+1))), randint(int(0)+1, int(relativec(timer))+1), width/randint(1, timer+1), True, \
                        False])
            screen.blit(runner, (width/5, runner_y-width/5))
            render_text('Game over!', (0, 0), font=titlefont)
            render_text(f'Your score was {score}.', (0, width/5-width/20))
            render_text('Press left joystick to play again.', (0, width/5))
            pg.display.update()
            clock.tick(100)
            timer += 1

if __name__ == '__main__':
    play(pg.display.set_mode((400, 400)), Controller())