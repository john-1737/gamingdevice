"""Hungry Robots, by Al Sweigart al@inventwithpython.com
Escape the hungry robots by making them crash into each other.
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: large, game"""

import random, sys
import pygame as pg
from pygame.locals import *
from tkinter import messagebox
try:
    from controller_mac import Controller
except ModuleNotFoundError:
    from controller_pi import Controller
from time import sleep

# Set up the constants:
WIDTH = 40           # (!) Try changing this to 70 or 10.
HEIGHT = 25          # (!) Try changing this to 10.
NUM_ROBOTS = 10      # (!) Try changing this to 1 or 30.
NUM_TELEPORTS = 2    # (!) Try changing this to 0 or 9999.
NUM_DEAD_ROBOTS = 2  # (!) Try changing this to 0 or 20.
NUM_WALLS = 100      # (!) Try changing this to 0 or 300.

EMPTY_SPACE = ' '    # (!) Try changing this to '.'.
PLAYER = '@'         # (!) Try changing this to 'R'.
ROBOT = 'R'          # (!) Try changing this to '@'.
DEAD_ROBOT = 'X'     # (!) Try changing this to 'R'.
pg.init()
pg.font.init()


# (!) Try changing this to '#' or 'O' or ' ':
WALL = chr(9617)  # Character 9617 is '░'
name = 'Hungry Robots'
image = 'hungryrobots.png'
help = '''Welcome to Hungry Robots!
In this game, you must fight
an army of hungry robots by
making them crash into each
other or dead robots.'''

def play(s, c):
    global screen, avatars, avatar, robot, dead_robot, font, small_font, width, render_text, get_joystick_value, button_pressed

    screen = s
    get_joystick_value, button_pressed = c.get_joystick_value, c.button_pressed
    width = screen.get_width()
    pg.display.set_caption('Hungry Robots')
    avatars = [pg.image.load('boy.png').convert_alpha(), pg.image.load('girl.png').convert_alpha()]
    lavatars = [pg.image.load('boy2.png').convert_alpha(), pg.image.load('girl2.png').convert_alpha()]
    lavatars = [pg.transform.scale(i, (width/16, width/16)) for i in lavatars]
    avatars = [pg.transform.scale(i, (width/40, width/40)) for i in lavatars]
    robot = pg.transform.scale(pg.image.load('robot2.png').convert_alpha(), (width/40, width/40))
    robotl = pg.transform.scale(pg.image.load('robot2.png').convert_alpha(), (width/16, width/16))
    dead_robotl = pg.transform.scale(pg.image.load('dead robot2.png').convert_alpha(), (width/16, width/16))
    dead_robot = pg.transform.scale(pg.image.load('dead robot2.png').convert_alpha(), (width/40, width/40))
    font = pg.font.SysFont(None, int(width/15))
    small_font = pg.font.SysFont(None, int(width/31))
    avatar = 0
    start = True
        
    def render_text(text, pos, font=font, color=(255, 255, 255), bold=True):
        text_surface = font.render(text, bold, color)
        screen.blit(text_surface, pos)
    sleep(0.2)
    while start:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
        val = get_joystick_value(0, 0)
        if abs(val) >= 75:
            if val <= 0:
                avatar = 0
            else:
                avatar = 1
        if button_pressed(1):
            return
        elif button_pressed(4):
            start = False
        screen.fill((0,0,0))
        render_text("Welcome to Hungry Robots!", (0,0), font=small_font)
        render_text("You are trapped in a maze with hungry robots! You don't know why robots", (0,width/32), font=small_font)
        render_text("need to eat, but you don't want to find out. The robots are badly", (0,width/32*2), font=small_font)
        render_text("programmed and will move directly toward you, even if blocked by walls.", (0,width/32*3), font=small_font)
        render_text("You must trick the robots into crashing into each other (or dead robots)", (0,width/32*4), font=small_font)
        render_text("without being caught. You have a personal teleporter device, but it only", (0,width/32*5), font=small_font)
        render_text(f"has enough battery for {NUM_TELEPORTS} trips. Keep in mind, you and robots can slip", (0,width/32*6), font=small_font)
        render_text("through the corners of two diagonal walls!", (0,width/32*7), font=small_font)
        screen.blit(robotl, (0,width/32*8))
        render_text(": robot", (width/16, width/32*8))
        screen.blit(dead_robotl, (0,width/32*10))
        render_text(": dead robot", (width/16, width/32*10))
        render_text('This is your avatar:', (0, width/32*12))
        screen.blit(lavatars[avatar], (0, width/32*14))
        render_text('You can change it by moving the left joystick', (0, width/32*16))
        render_text('left and right.', (0, width/32*18))
        render_text('Press left joystick to start!', (0, width/32*20))
        pg.display.update()
    sleep(0.2)
    # Set up a new game:
    while True:
        board = getNewBoard()
        robots = addRobots(board)
        playerPosition = getRandomEmptySpace(board, robots)
        lives = 3
        playing = True
        while lives and playing:  # Main game loop.
            move = set()
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    exit()

            if button_pressed(1):
                return
            elif button_pressed(4):
                move.add('C')
                sleep(0.2)
            elif button_pressed(0):
                move.add('T')
                sleep(0.2)

            axis_x = get_joystick_value(0, 0)
            axis_y = -get_joystick_value(0, 1)
            
            # --- Check for directional movement (one square per press) ---
            # Check for horizontal movement
            if abs(axis_x) > 50 and last_move_x == 0:
                dx = 'E' if axis_x > 0 else 'W'
                dy = None
                # Check for diagonal movement with vertical axis
                if abs(axis_y) > 50:
                    dy = 'S' if axis_y > 0 else 'N'
                move.add(dx)
                move.add(dy)
                sleep(0.2)
            
            # Check for vertical movement (only if not already moving horizontally)
            elif abs(axis_y) > 50 and last_move_y == 0:
                dy = 'S' if axis_y > 0 else 'N'
                dx = None
                move.add(dx)
                move.add(dy)
                sleep(0.2)

            # Store the current joystick direction
            last_move_x = 1 if axis_x > 50 else (-1 if axis_x < -50 else 0)
            last_move_y = 1 if axis_y > 50 else (-1 if axis_y < -50 else 0)

            while None in move:
                move.remove(None)

            playerPosition, move_made = askForPlayerMove(board, robots, playerPosition, move)
            if move_made:
                robots = moveRobots(board, robots, playerPosition)
            screen.fill((0,0,0))
            displayBoard(board, robots, playerPosition)
            render_text(f'Lives: {lives}', (0,0))
            render_text(f'Robots left: {len(robots)}', (width/2,0))
            render_text(f'Teleports left: {board["teleports"]}', (0, width/16))
            render_text('Use left joystick to move up, down, left, right,', (0, width/16*12))
            render_text('and diagonally.', (0, width/16*13))
            render_text('Press left joystick to stay still.', (0, width/16*14))
            if board['teleports'] > 0:
                render_text('Press triangle to teleport.', (0, width/16*15))
            if len(robots) == 0:  # Check if the player has won.
                playing = False

            for x, y in robots:  # Check if the player has lost.
                if (x, y) == playerPosition:
                    robots.remove((x, y))
                    lives -= 1
            pg.display.update()

        end = True
        while end:
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    exit()
            if button_pressed(1):
                return
            elif button_pressed(4):
                end = False
                sleep(0.2)
            screen.fill((0,0,0))
            displayBoard(board, robots, playerPosition)
            render_text(f'Lives: {lives}', (0,0))
            render_text(f'Robots left: {len(robots)}', (width/2,0))
            render_text(f'Teleports left: {board["teleports"]}', (0, width/16))
            if playing:
                render_text('You have run out of lives!', (0, width/16*12))
            else:
                render_text('All the robots have crashed into each other and', (0, width/16*12))
                render_text('you lived to tell the tale! Good job!', (0, width/16*13))
            render_text('Press left joystick to play again.', (0, width/16*14))
            pg.display.update()

def getNewBoard():
    """Returns a dictionary that represents the board. The keys are
    (x, y) tuples of integer indexes for board positions, the values are
    WALL, EMPTY_SPACE, or DEAD_ROBOT. The dictionary also has the key
    'teleports' for the number of teleports the player has left.
    The living robots are stored separately from the board dictionary."""
    board = {'teleports': NUM_TELEPORTS}

    # Create an empty board:
    for x in range(WIDTH):
        for y in range(HEIGHT):
            board[(x, y)] = EMPTY_SPACE

    # Add walls on the edges of the board:
    for x in range(WIDTH):
        board[(x, 0)] = WALL  # Make top wall.
        board[(x, HEIGHT - 1)] = WALL  # Make bottom wall.
    for y in range(HEIGHT):
        board[(0, y)] = WALL  # Make left wall.
        board[(WIDTH - 1, y)] = WALL  # Make right wall.

    # Add the random walls:
    for i in range(NUM_WALLS):
        x, y = getRandomEmptySpace(board, [])
        board[(x, y)] = WALL

    # Add the starting dead robots:
    for i in range(NUM_DEAD_ROBOTS):
        x, y = getRandomEmptySpace(board, [])
        board[(x, y)] = DEAD_ROBOT
    return board


def getRandomEmptySpace(board, robots):
    """Return a (x, y) integer tuple of an empty space on the board."""
    while True:
        randomX = random.randint(1, WIDTH - 2)
        randomY = random.randint(1, HEIGHT - 2)
        if isEmpty(randomX, randomY, board, robots):
            break
    return (randomX, randomY)


def isEmpty(x, y, board, robots):
    """Return True if the (x, y) is empty on the board and there's also
    no robot there."""
    return board[(x, y)] == EMPTY_SPACE and (x, y) not in robots


def addRobots(board):
    """Add NUM_ROBOTS number of robots to empty spaces on the board and
    return a list of these (x, y) spaces where robots are now located."""
    robots = []
    for i in range(NUM_ROBOTS):
        x, y = getRandomEmptySpace(board, robots)
        robots.append((x, y))
    return robots


def displayBoard(board, robots, playerPosition):
    """Display the board, robots, and player on the screen."""
    # Loop over every space on the board:
    for y in range(HEIGHT):
        for x in range(WIDTH):
            # Draw the appropriate character:
            if board[(x, y)] == WALL:
                pg.draw.rect(screen, (255, 255, 255), pg.Rect(x*width/40, (y*width/40)+width/8, width/40, width/40))
            elif board[(x, y)] == DEAD_ROBOT:
                screen.blit(dead_robot, (x*width/40, (y*width/40)+width/8))
            elif (x, y) == playerPosition:
                screen.blit(avatars[avatar], (x*width/40, (y*width/40)+width/8))
            elif (x, y) in robots:
                screen.blit(robot, (x*width/40, (y*width/40)+width/8))


def askForPlayerMove(board, robots, playerPosition, move):
    """Returns the (x, y) integer tuple of the place the player moves
    next, given their current location and the walls of the board."""
    playerX, playerY = playerPosition

    # Find which directions aren't blocked by a wall:
    q = {'N', 'W'} if isEmpty(playerX - 1, playerY - 1, board, robots) else {}
    w = {'N'} if isEmpty(playerX + 0, playerY - 1, board, robots) else {}
    e = {'N', 'E'} if isEmpty(playerX + 1, playerY - 1, board, robots) else {}
    d = {'E'} if isEmpty(playerX + 1, playerY + 0, board, robots) else {}
    c = {'S', 'E'} if isEmpty(playerX + 1, playerY + 1, board, robots) else {}
    x = {'S'} if isEmpty(playerX + 0, playerY + 1, board, robots) else {}
    z = {'S', 'W'} if isEmpty(playerX - 1, playerY + 1, board, robots) else {}
    a = {'W'} if isEmpty(playerX - 1, playerY + 0, board, robots) else {None}
    allMoves = (q , w , e , d , c , x , a , z)
        
    if 'T' in move and board['teleports'] > 0:
        # Teleport the player to a random empty space:
        board['teleports'] -= 1
        return getRandomEmptySpace(board, robots), True
    elif 'C' in move:
        return (playerX, playerY), True
    elif move != {} and move in allMoves:
        # Return the new player position based on their move:
        return {frozenset({'N', 'W'}): (playerX - 1, playerY - 1),
                frozenset({'N'}): (playerX + 0, playerY - 1),
                frozenset({'N', 'E'}): (playerX + 1, playerY - 1),
                frozenset({'E'}): (playerX + 1, playerY + 0),
                frozenset({'S', 'E'}): (playerX + 1, playerY + 1),
                frozenset({'S'}): (playerX + 0, playerY + 1),
                frozenset({'S', 'W'}): (playerX - 1, playerY + 1),
                frozenset({'W'}): (playerX - 1, playerY + 0)}[frozenset(move)], True
    return (playerX, playerY), False


def moveRobots(board, robotPositions, playerPosition):
    """Return a list of (x, y) tuples of new robot positions after they
    have tried to move toward the player."""
    playerx, playery = playerPosition
    nextRobotPositions = []

    while len(robotPositions) > 0:
        robotx, roboty = robotPositions[0]

        # Determine the direction the robot moves.
        if robotx < playerx:
            movex = 1  # Move right.
        elif robotx > playerx:
            movex = -1  # Move left.
        elif robotx == playerx:
            movex = 0  # Don't move horizontally.

        if roboty < playery:
            movey = 1  # Move up.
        elif roboty > playery:
            movey = -1  # Move down.
        elif roboty == playery:
            movey = 0  # Don't move vertically.

        # Check if the robot would run into a wall, and adjust course:
        if board[(robotx + movex, roboty + movey)] == WALL:
            # Robot would run into a wall, so come up with a new move:
            if board[(robotx + movex, roboty)] == EMPTY_SPACE:
                movey = 0  # Robot can't move horizontally.
            elif board[(robotx, roboty + movey)] == EMPTY_SPACE:
                movex = 0  # Robot can't move vertically.
            else:
                # Robot can't move.
                movex = 0
                movey = 0
        newRobotx = robotx + movex
        newRoboty = roboty + movey

        if (board[(robotx, roboty)] == DEAD_ROBOT
            or board[(newRobotx, newRoboty)] == DEAD_ROBOT):
            # Robot is at a crash site, remove it.
            del robotPositions[0]
            continue

        # Check if it moves into a robot, then destroy both robots:
        if (newRobotx, newRoboty) in nextRobotPositions:
            board[(newRobotx, newRoboty)] = DEAD_ROBOT
            nextRobotPositions.remove((newRobotx, newRoboty))
        else:
            nextRobotPositions.append((newRobotx, newRoboty))

        # Remove robots from robotPositions as they move.
        del robotPositions[0]
    return nextRobotPositions



# If this program was run (instead of imported), run the game:
if __name__ == '__main__':
    play(pg.display.set_mode((600, 600)), Controller())