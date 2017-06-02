# Import a library of functions called 'pygame'
import pygame
import math
import bot
import random

board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
turn = 1



# table1 = bot.initValueTable(1)
# table2 = bot.initValueTable(2)

table2 = bot.load_obj('table2')
table1 = bot.load_obj('table1')

def checkWin(playerNum):
    for i in range(0, 3):
        count = 0
        for j in range(0, 3):
            if (board[i][j] == playerNum): count += 1
        if (count == 3): return True
    for i in range(0, 3):
        count = 0
        for j in range(0, 3):
            if (board[j][i] == playerNum): count += 1
        if (count == 3): return True
    count = 0
    for i in range(0, 3):
        if (board[i][i] == playerNum): count += 1
        if (count == 3): return True
    count = 0
    for i in range(0, 3):
        if (board[i][2 - i] == playerNum): count += 1
        if (count == 3): return True
    return False

def drawBoard():
    pygame.draw.line(screen, BLACK, [200, 0], [200,600], 5)
    pygame.draw.line(screen, BLACK, [400, 0], [400,600], 5)
    pygame.draw.line(screen, BLACK, [0, 200], [600,200], 5)
    pygame.draw.line(screen, BLACK, [0, 400], [600,400], 5)
    for i in range(0, 3):
        for j in range(0, 3):
            if (board[i][j] != 0): drawMove(board[i][j], [i, j])

def drawMove(playerNum, pos):
    drawPosX = pos[0] * 200 + 100
    drawPosY = pos[1] * 200 + 100
    if (playerNum == 1):
        pygame.draw.line(screen, RED, [drawPosX + 20, drawPosY + 20], [drawPosX - 20, drawPosY - 20], 5)
        pygame.draw.line(screen, RED, [drawPosX - 20, drawPosY + 20], [drawPosX + 20, drawPosY - 20], 5)
    elif (playerNum == 2):
        pygame.draw.circle(screen, BLUE, [drawPosX, drawPosY], 40)
    pygame.display.flip()

def inputMove(playerNum, mousePos):
    posX = math.floor(mousePos[0]/200)
    posY = math.floor(mousePos[1]/200)
    if (board[int(posX)][int(posY)] != 0):
        print("Invalid move")
        return 0
    playMove(playerNum, [int(posX), int(posY)])
    return 1

def playMove(playerNum, pos):
    board[pos[0]][pos[1]] = playerNum

def checkReset():
    global turn, board
    if (checkWin(turn)):
        print("Player " + str(turn) + " wins")
        board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        turn = 1
    else:
        full = True
        for i in range(3):
            for j in range(3):
                if (board[i][j] == 0): full = False
        if (full):
            print("Tie game")
            board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            turn = 1
        else:
            turn = 2 - (turn + 1) % 2

def playerTurn():
    oldBoard = bot.getBoardString(board)
    if (inputMove(turn, event.pos) == 0): return
    # print(oldBoard)
    # print(board)
    bot.updateValues(table2, oldBoard, bot.getBoardString(board))
    checkReset()

def randomTurn():
    oldBoard = bot.getBoardString(board)
    open = []
    for i in range(3):
        for j in range(3):
            if (board[i][j] == 0): open.append([i, j])
    playMove(turn, open[random.randint(0, len(open) - 1)])
    bot.updateValues(table1, oldBoard, bot.getBoardString(board))
    checkReset()

def botTurn():
    oldBoard = bot.getBoardString(board)
    table = table1
    opTable = table2
    if (turn == 2):
        table = table2
        opTable = table1
    move = bot.getBestMove(table, board, turn)
    playMove(turn, move)
    bot.updateValues(opTable, oldBoard, bot.getBoardString(board))
    # print(opTable[bot.getBoardString(board)])
    checkReset()

def botTurnSingle():
    oldBoard = bot.getBoardString(board)
    move = bot.getBestMove(table2, board, turn)
    playMove(turn, move)
    bot.updateValues(table2, oldBoard, bot.getBoardString(board))
    # print(opTable[bot.getBoardString(board)])
    checkReset()


# Initialize the game engine
pygame.init()

# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

# Set the height and width of the screen
size = [600, 600]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Example code for the draw module")

#Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()


while not done:

    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(10)

    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            bot.save_obj(table1, 'table1')
            bot.save_obj(table2, 'table2')
            done=True # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONUP:
            if (turn==1):
                playerTurn()

    if (turn == 2):
        botTurnSingle()

    # botTurn()



    screen.fill(WHITE)
    drawBoard()



    pygame.display.flip()

# Be IDLE friendly
pygame.quit()
