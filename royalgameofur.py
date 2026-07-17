"""The Royal Game of Ur, by Al Sweigart al@inventwithpython.com
A 5,000 year old board game from Mesopotamia. Two players knock each
other back as they race for the goal.
More info https://en.wikipedia.org/wiki/Royal_Game_of_Ur
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: large, board game, game, two-player
"""

import random, sys
import pygame as pg
from pygame.locals import *
try:
    from controller_mac import Controller
except ModuleNotFoundError:
    from controller_pi import Controller
controller = Controller() #Create a Controller object.
get_joystick_value, button_pressed = controller.get_joystick_value, controller.button_pressed
from time import sleep
pg.init()

X_PLAYER = 'X'
O_PLAYER = 'O'
EMPTY = ' '
WHITE, RED, BLUE, BLACK, YELLOW, GREEN = (255, 255, 255), (255, 0, 0), (0, 0, 255), (0, 0, 0), (255, 255, 0), (0, 200, 0)

pg.font.init()

name = 'Royal Game of Ur'
help = '''Welcome to Royal Game of Ur!
This is a 5,000 year old racing
game were you must race your
tokens to the finish line before
your opponent.
This is a 2-player game.'''
image = 'royalgameofur.png'

# Set up constants for the space labels:
X_HOME = 'x_home'
O_HOME = 'o_home'
X_GOAL = 'x_goal'
O_GOAL = 'o_goal'

# The spaces in left to right, top to bottom order:
ALL_SPACES = 'hgfetsijklmnopdcbarq'
SPACE_POSITIONS = 'hgfe  tsijklmnopdcba  rq'
X_TRACK = 'HefghijklmnopstG'  # (H stands for Home, G stands for Goal.)
O_TRACK = 'HabcdijklmnopqrG'

FLOWER_SPACES = ('h', 't', 'l', 'd', 'r')

def play(s):
    global flower, screen, width, small_font, font, render_text
    screen = s
    width = screen.get_width()
    small_font = pg.font.SysFont(None, int(width/16))
    font = pg.font.SysFont(None, int(width/8))
    hints_mode = False
    path_mode = False
    flower = pg.transform.scale(pg.image.load('flower.png').convert_alpha(), (width/8, width/8))
    start_screen = True
    
    def render_text(text, pos, font=font, color=WHITE, bold=True):
        text_surface = font.render(text, bold, color)
        screen.blit(text_surface, pos)
    
    sleep(0.2)
    while start_screen:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
        if button_pressed(4):
            start_screen = False
        elif button_pressed(2):
            sleep(0.2)
            help = True
            while help:
                for event in pg.event.get():
                    if event.type == QUIT:
                        pg.quit()
                        sys.exit()
                if button_pressed(4):
                    start_screen = False
                elif button_pressed(2):
                    help = False
                elif button_pressed(1):
                    return
                screen.fill(BLACK)
                render_text('Welcome to Royal Game of Ur!', pos=(0, 0), font=small_font)
                render_text('Inspired by Al Sweigart\'s Royal Game Of Ur.', pos=(0, w/16*15), font=small_font)

                render_text('This is a 5,000 year old game. Two players must', pos=(0, w/16), font=small_font)
                render_text('move their tokens from their home to their goal.', pos=(0,w/16*2), font=small_font)
                render_text('On your turn you roll four dice and can move one', pos=(0 ,w/16*3), font=small_font)

                render_text('token a number of spaces equal to the points you', pos=(0, w/16*4), font=small_font)
                render_text('got. Ur is a racing game; the first player to move', pos=(0, w/16*5), font=small_font)

                render_text('all seven of their tokens to their goal wins.', pos=(0, w/16*6), font=small_font)
            
                render_text('To do this, tokens must travel from their home to', pos=(0, w/16*7), font=small_font)
                render_text('their goal using the above path. If you land on an', pos=(0, w/16*8), font=small_font)
                render_text('opponent\'s token in the middle track, it gets sent', pos=(0, w/16*9), font=small_font)
                render_text('back home. The flower spaces let you take', pos=(0, w/16*10), font=small_font)
                render_text('another turn. Tokens in the middle flower space', pos=(0, w/16*11), font=small_font)
                render_text('are safe and cannot be landed on. Player 1 uses', pos=(0, w/16*12), font=small_font)
                render_text('the left joystick and player 2 uses the right.', pos=(0, w/16*13), font=small_font)
                render_text('Press the circle button to exit this menu.', pos=(0, w/16*15), font=small_font)
                pg.display.update()
            sleep(0.2)
        elif button_pressed(1):
            return
        screen.fill(BLACK)
        displayBoard(getNewBoard(), sides=False)
        show_path()
        w = width # Line shortening.
        render_text('Welcome to Royal Game of Ur!', pos=(0, 0), font=small_font)
        render_text('Inspired by Al Sweigart\'s Royal Game Of Ur.', pos=(0, w/16), font=small_font)

        render_text('This is a 5,000 year old game. Two players must', pos=(0, w/2), font=small_font)
        render_text('move their tokens from their home to their goal.', pos=(0,w/16*9), font=small_font)
        render_text('On your turn you roll four dice and can move one', pos=(0 ,w/16*10), font=small_font)

        render_text('token a number of spaces equal to the points you', pos=(0, w/16*11), font=small_font)
        render_text('got. Ur is a racing game; the first player to move', pos=(0, w/16*12), font=small_font)

        render_text('all seven of their tokens to their goal wins.', pos=(0, w/16*13), font=small_font)
        render_text('Press left joystick to start the game.', pos=(0, w/16*14), font=small_font)
        render_text('Press circle for more info.', pos=(0, w/16*15), font=small_font)
        pg.display.update()
    sleep(0.2)
    while True:
        turn = O_PLAYER
        status = 'normal'
        gameBoard = getNewBoard()
        flips = []
        flipTally = 0
        for i in range(4):
            result = random.randint(0, 1)
            flips.append(result)
            flipTally += result
        lost_turn = False
        playing = True
        x, y = 0, 0
        while playing:  # Main game loop.
            # Set up some variables for this turn:
            if turn == X_PLAYER:
                opponent = O_PLAYER
                home = X_HOME
                track = X_TRACK
                goal = X_GOAL
                opponentHome = O_HOME
            elif turn == O_PLAYER:
                opponent = X_PLAYER
                home = O_HOME
                track = O_TRACK
                goal = O_GOAL
                opponentHome = X_HOME
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
            new_x, new_y = x, y
            val = get_joystick_value(int(turn == O_PLAYER), 0)
            if abs(val) > 75:
                if val <= 0:
                    new_x -= 1
                    sleep(0.2)
                else:
                    new_x += 1
                    sleep(0.2)
            val = get_joystick_value(int(turn == O_PLAYER), 1)
            if abs(val) > 75:
                if val <= 0:
                    new_y += 1
                    sleep(0.2)
                else:
                    new_y -= 1
                    sleep(0.2)                    
            if new_x in (4, 5) and new_y in (1, 3):
                pass
            elif new_x in (4, 5, 6, 7) and new_y in (0, 4):
                pass
            elif new_x in (1, 2, 3) and new_y == 0:
                x, y = 0, 0
            elif new_x in (1, 2, 3) and new_y == 4:
                x, y = 0, 4
            elif new_x < 0:
                x, y = 0, new_y
            elif new_x > 7:
                x, y = 7, new_y
            elif new_y < 0:
                x, y = new_x, 0
            elif new_y > 4:
                x, y = new_x, 4
            else:
                x, y = new_x, new_y
            if button_pressed(4 if turn == X_PLAYER else 5) and not status == 'win':
                for i in range(1):
                    if lost_turn == True:
                        turn = opponent
                        flips = []
                        flipTally = 0
                        for i in range(4):
                            result = random.randint(0, 1)
                            flips.append(result)
                            flipTally += result
                        status='normal'
                        lost_turn = False
                        sleep(0.2)
                        break
                    if x in (8, 9):
                        break
                    # Perform the selected move on the board:
                    if y in (0, 4) and x in (0, 1, 2, 3) and 'home' in validMoves:
                        # Subtract tokens at home if moving from home:
                        gameBoard[home] -= 1
                        nextTrackSpaceIndex = flipTally
                        nextBoardSpace = track[nextTrackSpaceIndex]
                        # Check if the opponent has a tile there:
                        if gameBoard[nextBoardSpace] == opponent:
                            gameBoard[opponentHome] += 1
                        gameBoard[nextBoardSpace] = turn
                        flips = []
                        flipTally = 0
                        for i in range(4):
                            result = random.randint(0, 1)
                            flips.append(result)
                            flipTally += result
                        status='normal'
                        if nextBoardSpace in FLOWER_SPACES:
                            status = 'flower land'
                        else:
                            turn = opponent
                        sleep(0.2)
                        break
                    else:
                        pos = int(((y*8)+x)-8)
                        if pos < 0 or pos > 23:
                            break
                        move = SPACE_POSITIONS[pos]
                        if move not in validMoves:
                            break
                        gameBoard[move] = EMPTY  # Set the "from" space to empty.
                        nextTrackSpaceIndex = track.index(move) + flipTally

                    movingOntoGoal = nextTrackSpaceIndex == len(track) - 1
                    if movingOntoGoal:
                        gameBoard[goal] += 1
                        # Check if the player has won:
                        if gameBoard[goal] == 1:
                            displayBoard(gameBoard)
                            status = 'win'
                            break
                        nextBoardSpace = 'z'
                    else:
                        nextBoardSpace = track[nextTrackSpaceIndex]
                        # Check if the opponent has a tile there:
                        if gameBoard[nextBoardSpace] == opponent:
                            gameBoard[opponentHome] += 1
                        gameBoard[nextBoardSpace] = turn

                    # Check if the player landed on a flower space and can go again:
                
                    if nextBoardSpace in FLOWER_SPACES:
                        status = 'flower land'
                    else:
                        turn = opponent
                        status='normal'

                    flips = []
                    flipTally = 0
                    for i in range(4):
                        result = random.randint(0, 1)
                        flips.append(result)
                        flipTally += result
                    sleep(0.2)
                    
            if button_pressed(2):
                path_mode = not path_mode
                sleep(0.2)
            if button_pressed(0):
                hints_mode = not hints_mode
                sleep(0.2)
            elif button_pressed(4) and status == 'win':
                playing = False
                sleep(0.2)
            elif button_pressed(1):
                return

            screen.fill(BLACK)
            displayBoard(gameBoard)
            color = {'X': 'red', 'O': 'blue'}
            if status == 'win':
                render_text(f'{color[turn]} wins!', (0, width/8*5))
                render_text('Press SPACE to play again.', (0, width/8*5), small_font)
                pg.display.update()
                continue
            if status == 'flower land':
                render_text(f'{color[turn]} landed on a flower space and gets to go', (0, width/8*5), small_font)
                render_text(f'again. Rolls:', (0, width/8*5+width/16), small_font)
            else:
                render_text('It is ' + color[turn] + '\'s turn. Rolls:', (0, width/8*5), font)
            for i in range(4): 
                pg.draw.polygon(screen, WHITE, ((((i*width/4)+width/8), width/8*6), (((i*width/4)+width/16), width/8*7), (((i*width/4)+width/16*3), width/8*7)))
                if flips[i] == 1:
                    pg.draw.circle(screen, BLACK, (((i*width/4)+width/8), width/8*6+width/32*3), width/32, width=0)
            if flipTally == 0:
                render_text('You didn\'t roll any points, so you lose a turn.', (0, width/8*7), small_font)
                lost_turn = True
                pg.display.update()
                continue
            
            # Ask the player for their move:
            validMoves = getValidMoves(gameBoard, turn, flipTally)
            if hints_mode:
                show_hints(turn, validMoves)
            if path_mode:
                show_path()
            if (x, y) == (0, 0):
                pg.draw.rect(screen, YELLOW, pg.Rect(x*width/8, y*width/8, width/2, width/8), 2)
            elif (x, y) == (0, 4):
                pg.draw.rect(screen, YELLOW, pg.Rect(x*width/8, y*width/8, width/2, width/8), 2)
            else:
                pg.draw.rect(screen, YELLOW, pg.Rect(x*width/8, y*width/8, width/8, width/8), 2)

            if validMoves == []:
                render_text('There are no possible moves, so you lose a turn.', (0, width/8*7), font)
                lost_turn = True
                pg.display.update()
                continue
        
            render_text('Select token or home to move '+ str(flipTally)+ ' spaces.', (0, width/8*7), small_font)
            render_text(f'Press triangle to {"hide" if hints_mode else "show"} all possible moves.', (0, width/8*7+width/16), small_font)
            pg.display.update()
            # Swap turns to the other player.
        sleep(0.2)

def getNewBoard():
    """
    Returns a dictionary that represents the state of the board. The
    keys are strings of the space labels, the values are X_PLAYER,
    O_PLAYER, or EMPTY. There are also counters for how many tokens are
    at the home and goal of both players.
    """
    board = {X_HOME: 7, X_GOAL: 0, O_HOME: 7, O_GOAL: 0}
    # Set each space as empty to start:
    for spaceLabel in ALL_SPACES:
        board[spaceLabel] = EMPTY
    return board

def show_path():
    c = lambda x, y: ((x-100)/100*width/8+width/8, (y-100)/100*width/8+width/8)
    for i in (100, 200, 300, 400, 500, 600, 700):
        pg.draw.polygon(screen, RED, (c(i-15, 210), c(i-15, 240), c(i+15, 225)))
        pg.draw.polygon(screen, BLUE, (c(i-15, 260), c(i-15, 290), c(i+15, 275)))
        if i not in (400, 500, 600):
            pg.draw.polygon(screen, RED, (c(i+15, 135), c(i+15, 165), c(i-15, 150)))
            pg.draw.polygon(screen, BLUE, (c(i+15, 335), c(i+15, 365), c(i-15, 350)))
    pg.draw.polygon(screen, RED, (c(35, 185), c(65, 185), c(50, 215)))
    pg.draw.polygon(screen, RED, (c(735, 215), c(765, 215), c(750, 185)))
    pg.draw.polygon(screen, RED, (c(335, 85), c(365, 85), c(350, 115)))
    pg.draw.polygon(screen, RED, (c(635, 115), c(665, 115), c(650, 85)))
    pg.draw.polygon(screen, BLUE, (c(35, 315), c(65, 315), c(50, 285)))
    pg.draw.polygon(screen, BLUE, (c(735, 285), c(765, 285), c(750, 315)))
    pg.draw.polygon(screen, BLUE, (c(335, 415), c(365, 415), c(350, 385)))
    pg.draw.polygon(screen, BLUE, (c(635, 385), c(665, 385), c(650, 415)))

def displayBoard(board, sides=True):
    """Display the board on the screen."""
    c = lambda x, y: ((x-100)/100*width/8+width/8, (y-100)/100*width/8+width/8)
    for i in (c(0, 100), c(600, 100), c(0, 300), c(600, 300), c(300, 200)):
        screen.blit(flower, i)
    for i in range(0, 9):
        if i == 5:
            pg.draw.line(screen, WHITE, c(500, 200), c(500, 300), 5)
        else:
            pg.draw.line(screen, WHITE, c((i*100), 100), c((i*100), 400), 5)
    for i in range(1, 5):
        if i in (2, 3):
            pg.draw.line(screen, WHITE, c(0, (i*100)), c(800, (i*100)), 5)
        else:
            pg.draw.line(screen, WHITE, c(0, (i*100)), c(400, (i*100)), 5)
            pg.draw.line(screen, WHITE, c(600, (i*100)), c(800, (i*100)), 5)
    if not sides:
        return
    for i in range(7):
        pg.draw.circle(screen, WHITE, c((50+(i*50)), 50), width/32, width=5)
        pg.draw.circle(screen, WHITE, c((50+(i*50)), 450), width/32, width=5)
        pg.draw.circle(screen, WHITE, c((450+(i*50)), 50), width/32, width=5)
        pg.draw.circle(screen, WHITE, c((450+(i*50)), 450), width/32, width=5)
    for i in range(7):
        if i < board[X_HOME]:
            pg.draw.circle(screen, RED, c((50+(i*50)), 50), width/32, width=0)
        if i < board[O_HOME]:
            pg.draw.circle(screen, BLUE, c((50+(i*50)), 450), width/32, width=0)
        if i < board[X_GOAL]:
            pg.draw.circle(screen, RED, c((450+(i*50)), 50), width/32, width=0)        
        if i < board[O_GOAL]:
            pg.draw.circle(screen, BLUE, c((450+(i*50)), 450), width/32, width=0)
    for i, s in enumerate(SPACE_POSITIONS):
        y, x = divmod(i, 8)
        y *= 100
        y += 150
        x *= 100
        x += 50
        if s == ' ':
            continue
        if board[s] == ' ':
            continue
        if board[s] == X_PLAYER:
            fill = RED
        elif board[s] == O_PLAYER:
            fill = BLUE
        pg.draw.circle(screen, fill, c(x, y), width/32, width=0)
    render_text('red home', (0, 0), small_font, RED, False)
    render_text('blue home', (0, width/32*19), small_font, BLUE, False)
    render_text('red goal', (width/2, 0), small_font, RED, False)
    render_text('blue goal', (width/2, width/32*19), small_font, BLUE, False)


def show_hints(player, moves):
    c = lambda x, y: ((x-100)/100*width/8+width/8, (y-100)/100*width/8+width/8)
    if 'home' in moves:
        if player == X_PLAYER:
            pos = 0
        else:
            pos = width/2
        pg.draw.rect(screen, GREEN, pg.Rect(0, pos, width/2, width/8), 5)
    for i, s in enumerate(SPACE_POSITIONS):
        y, x = divmod(i, 8)
        y *= width/8
        y += width/8
        x *= width/8
        if s == ' ':
            continue
        if s in moves:
            pg.draw.rect(screen, GREEN, pg.Rect(x, y, width/8, width/8), 5)


def getValidMoves(board, player, flipTally):
    validMoves = []  # Contains the spaces with tokens that can move.
    if player == X_PLAYER:
        opponent = O_PLAYER
        track = X_TRACK
        home = X_HOME
    elif player == O_PLAYER:
        opponent = X_PLAYER
        track = O_TRACK
        home = O_HOME

    # Check if the player can move a token from home:
    if board[home] > 0 and board[track[flipTally]] == EMPTY:
        validMoves.append('home')

    # Check which spaces have a token the player can move:
    for trackSpaceIndex, space in enumerate(track):
        if space == 'H' or space == 'G' or board[space] != player:
            continue
        nextTrackSpaceIndex = trackSpaceIndex + flipTally
        if nextTrackSpaceIndex >= len(track):
            # You must flip an exact number of moves onto the goal,
            # otherwise you can't move on the goal.
            continue
        else:
            nextBoardSpaceKey = track[nextTrackSpaceIndex]
            if nextBoardSpaceKey == 'G':
                # This token can move off the board:
                validMoves.append(space)
                continue
        if board[nextBoardSpaceKey] in (EMPTY, opponent):
            # If the next space is the protected middle space, you
            # can only move there if it is empty:
            if nextBoardSpaceKey == 'l' and board['l'] == opponent:
                continue  # Skip this move, the space is protected.
            validMoves.append(space)

    return validMoves


if __name__ == '__main__':
    play(pg.display.set_mode((400, 400)))