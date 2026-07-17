"""Twenty Forty-Eight, by Al Sweigart al@inventwithpython.com
A sliding tile game to combine exponentially-increasing numbers.
Inspired by Gabriele Cirulli's 2048, which is a clone of Veewo Studios'
1024, which in turn is a clone of the Threes! game.
More info at https://en.wikipedia.org/wiki/2048_(video_game)
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: large, game, puzzle"""

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

# Set up the constants:
BLANK = ''  # A value that represents a blank space on the board.

pg.init()

name = '2048'
help = '''Welcome to 2048!
This is a game where you
combine tiles to create
exponentially increasing
numbers.
This game is based on Al
Sweigart's 2048.'''
image = '2048.png'

colors = ((255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255), (255, 0, 255))

def play(s):
    global screen, font, smallfont, width
    screen = s
    width = screen.get_width()
    pg.font.init()
    font = pg.font.SysFont(None, int(width/9))
    smallfont = pg.font.SysFont(None, int(width/18))
    start_screen = True
    sleep(0.2)
    while start_screen:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
        if button_pressed(1):
            return
        elif button_pressed(4):
            start_screen = False
        screen.fill((0,0,0))
        render_text('Welcome to 2048 (Joystick Version)!', (0, 0), font=smallfont)
        render_text('Slide all the tiles on the board in one of four', (0, width/16), font=smallfont)
        render_text('directions with the left joystick.', (0, width/8), font=smallfont)
        render_text('Tiles with like numbers will combine into', (0, width/16*3), font=smallfont)
        render_text('larger-numbered tiles.', (0, width/4), font=smallfont)
        render_text('A new 2 tile is added to the board on each move.', (0, width/16*5), font=smallfont)
        render_text('You win if you can create a 2048 tile.', (0, width/16*6), font=smallfont)
        render_text('You lose if the board fills up the tiles before then.', (0, width/16*7), font=smallfont)
        render_text('Press left joystick to start!', (0, width/2), font=smallfont)
        pg.display.update()
        
    sleep(0.2)
    while True:
        gameBoard = getNewBoard()
        game = True
        while game:  # Main game loop.
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
            val = get_joystick_value(0, 0)
            if abs(val) > 75:
                if val <= 0:
                    gameBoard = makeMove(gameBoard, 'A')
                    addTwoToBoard(gameBoard)
                    sleep(0.2)
                else:
                    gameBoard = makeMove(gameBoard, 'D')
                    addTwoToBoard(gameBoard)
                    sleep(0.2)
            val = get_joystick_value(0, 1)
            if abs(val) > 75:
                if val >= 0:
                    gameBoard = makeMove(gameBoard, 'W')
                    addTwoToBoard(gameBoard)
                    sleep(0.2)      
                else:
                    gameBoard = makeMove(gameBoard, 'S')
                    addTwoToBoard(gameBoard)
                    sleep(0.2)
            if button_pressed(1):
                return
            elif button_pressed(2):
                gameBoard = getNewBoard()
                sleep(0.2)
            screen.fill((0,0,0))
            drawBoard(gameBoard)
            if isFull(gameBoard):
                game = False
            else:
                render_text('Score: '+ str(getScore(gameBoard)), (0, width/4*3), font)
                render_text('Press circle to reset.', (0, width/8*7), font=smallfont)
            pg.display.update()

        endgame = True
        while endgame:
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
            if button_pressed(1):
                return
            elif button_pressed(4):
                endgame = False
            screen.fill((0, 0, 0))
            drawBoard(gameBoard)
            render_text('Game Over!', (0, width/4*3), font)
            render_text(f'Your score was {getScore(gameBoard)}.', (0, width/8*7), font=smallfont)
            render_text('Press left joystick to play again.', (0, width/16*15), font=smallfont)
            pg.display.update()

def getNewBoard():
    """Returns a new data structure that represents a board.

    It's a dictionary with keys of (x, y) tuples and values of the tile
    at that space. The tile is either a power-of-two integer or BLANK.
    The coordinates are laid out as:
       X0 1 2 3
      Y+-+-+-+-+
      0| | | | |
       +-+-+-+-+
      1| | | | |
       +-+-+-+-+
      2| | | | |
       +-+-+-+-+
      3| | | | |
       +-+-+-+-+"""

    newBoard = {}  # Contains the board data structure to be returned.
    # Loop over every possible space and set all the tiles to blank:
    for x in range(4):
        for y in range(4):
            newBoard[(x, y)] = BLANK

    # Pick two random spaces for the two starting 2's:
    startingTwosPlaced = 0  # The number of starting spaces picked.
    while startingTwosPlaced < 2:  # Repeat for duplicate spaces.
        randomSpace = (random.randint(0, 3), random.randint(0, 3))
        # Make sure the randomly selected space isn't already taken:
        if newBoard[randomSpace] == BLANK:
            newBoard[randomSpace] = 2
            startingTwosPlaced = startingTwosPlaced + 1

    return newBoard

def drawBoard(board):
    """Draws the board data structure on the screen."""

    # Go through each possible space left to right, top to bottom, and
    # create a list of what each space's label should be.
    labels = []  # A list of strings for the number/blank for that tile.
    board_width = (width-width/4)
    for y in range(4):
        for x in range(4):
            tile = board[(x, y)]  # Get the tile at this space.
            pg.draw.rect(screen, (100, 100, 100), pg.Rect(x*board_width/4+width/8, y*board_width/4, board_width/4, board_width/4), 10)
            if tile != BLANK:
                num = 2
                color = 0
                while num != tile:
                    color += 1
                    num *= 2
                pg.draw.rect(screen, colors[color%6], pg.Rect(x*board_width/4+width/8, y*board_width/4, board_width/4, board_width/4))
                render_text(str(tile), ((x*board_width/4)+board_width/8+width/8, (y*board_width/4)+board_width/8), font, True, (0, 0, 0))

def getScore(board):
    """Returns the sum of all the tiles on the board data structure."""
    score = 0
    # Loop over every space and add the tile to the score:
    for x in range(4):
        for y in range(4):
            # Only add non-blank tiles to the score:
            if board[(x, y)] != BLANK:
                score = score + board[(x, y)]
    return score

def render_text(text, pos, font, center=False, color=(255, 255, 255)):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect()
    if center:
        width = rect.width/2
        height = rect.height/2
        screen.blit(text_surface, (pos[0]-width,  pos[1]-height))
    else:
        screen.blit(text_surface, pos)

def combineTilesInColumn(column):
    """The column is a list of four tile. Index 0 is the "bottom" of
    the column, and tiles are pulled "down" and combine if they are the
    same. For example, combineTilesInColumn([2, BLANK, 2, BLANK])
    returns [4, BLANK, BLANK, BLANK]."""

    # Copy only the numbers (not blanks) from column to combinedTiles
    combinedTiles = []  # A list of the non-blank tiles in column.
    for i in range(4):
        if column[i] != BLANK:
            combinedTiles.append(column[i])

    # Keep adding blanks until there are 4 tiles:
    while len(combinedTiles) < 4:
        combinedTiles.append(BLANK)

    # Combine numbers if the one "above" it is the same, and double it.
    for i in range(3):  # Skip index 3: it's the topmost space.
        if combinedTiles[i] == combinedTiles[i + 1]:
            combinedTiles[i] *= 2  # Double the number in the tile.
            # Move the tiles above it down one space:
            for aboveIndex in range(i + 1, 3):
                combinedTiles[aboveIndex] = combinedTiles[aboveIndex + 1]
            combinedTiles[3] = BLANK  # Topmost space is always BLANK.
    return combinedTiles


def makeMove(board, move):
    """Carries out the move on the board.

    The move argument is either 'W', 'A', 'S', or 'D' and the function
    returns the resulting board data structure."""

    # The board is split up into four columns, which are different
    # depending on the direction of the move:
    if move == 'W':
        allColumnsSpaces = [[(0, 0), (0, 1), (0, 2), (0, 3)],
                            [(1, 0), (1, 1), (1, 2), (1, 3)],
                            [(2, 0), (2, 1), (2, 2), (2, 3)],
                            [(3, 0), (3, 1), (3, 2), (3, 3)]]
    elif move == 'A':
        allColumnsSpaces = [[(0, 0), (1, 0), (2, 0), (3, 0)],
                            [(0, 1), (1, 1), (2, 1), (3, 1)],
                            [(0, 2), (1, 2), (2, 2), (3, 2)],
                            [(0, 3), (1, 3), (2, 3), (3, 3)]]
    elif move == 'S':
        allColumnsSpaces = [[(0, 3), (0, 2), (0, 1), (0, 0)],
                            [(1, 3), (1, 2), (1, 1), (1, 0)],
                            [(2, 3), (2, 2), (2, 1), (2, 0)],
                            [(3, 3), (3, 2), (3, 1), (3, 0)]]
    elif move == 'D':
        allColumnsSpaces = [[(3, 0), (2, 0), (1, 0), (0, 0)],
                            [(3, 1), (2, 1), (1, 1), (0, 1)],
                            [(3, 2), (2, 2), (1, 2), (0, 2)],
                            [(3, 3), (2, 3), (1, 3), (0, 3)]]

    # The board data structure after making the move:
    boardAfterMove = {}
    for columnSpaces in allColumnsSpaces:  # Loop over all 4 columns.
        # Get the tiles of this column (The first tile is the "bottom"
        # of the column):
        firstTileSpace = columnSpaces[0]
        secondTileSpace = columnSpaces[1]
        thirdTileSpace = columnSpaces[2]
        fourthTileSpace = columnSpaces[3]

        firstTile = board[firstTileSpace]
        secondTile = board[secondTileSpace]
        thirdTile = board[thirdTileSpace]
        fourthTile = board[fourthTileSpace]

        # Form the column and combine the tiles in it:
        column = [firstTile, secondTile, thirdTile, fourthTile]
        combinedTilesColumn = combineTilesInColumn(column)

        # Set up the new board data structure with the combined tiles:
        boardAfterMove[firstTileSpace] = combinedTilesColumn[0]
        boardAfterMove[secondTileSpace] = combinedTilesColumn[1]
        boardAfterMove[thirdTileSpace] = combinedTilesColumn[2]
        boardAfterMove[fourthTileSpace] = combinedTilesColumn[3]

    return boardAfterMove


def askForPlayerMove():
    """Asks the player for the direction of their next move (or quit).

    Ensures they enter a valid move: either 'W', 'A', 'S' or 'D'."""
    print('Enter move: (WASD or Q to quit)')
    while True:  # Keep looping until they enter a valid move.
        move = input('> ').upper()
        if move == 'Q':
            # End the program:
            print('Thanks for playing!')
            sys.exit()

        # Either return the valid move, or loop back and ask again:
        if move in ('W', 'A', 'S', 'D'):
            return move
        else:
            print('Enter one of "W", "A", "S", "D", or "Q".')


def addTwoToBoard(board):
    """Adds a new 2 tile randomly to the board."""
    while True:
        randomSpace = (random.randint(0, 3), random.randint(0, 3))
        if board[randomSpace] == BLANK:
            board[randomSpace] = 2
            return  # Return after finding one non-blank tile.


def isFull(board):
    """Returns True if the board data structure has no blanks."""
    # Loop over every space on the board:
    for x in range(4):
        for y in range(4):
            # If a space is blank, return False:
            if board[(x, y)] == BLANK:
                return False
    return True  # No space is blank, so return True.


# If this program was run (instead of imported), run the game:
if __name__ == '__main__':
    play(pg.display.set_mode(400, 400))
