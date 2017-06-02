import pickle

stepSize = 0.8


def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def isFull(boardString):
    full = True
    for i in range(9):
        if (boardString[i] == '0'): full = False
    return full


def initValueTable(player):
    table = {}
    keys = [(x1, x2, x3, x4, x5, x6, x7, x8, x9) for x1 in range(3) for x2 in range(3) for x3 in range(3) for x4 in range(3)for x5 in range(3)for x6 in range(3)for x7 in range(3) for x8 in range(3) for x9 in range(3)]
    for i in range(len(keys)):
        if checkWin(getBoard(getStringFromArray(keys[i])), player):
            table[getStringFromArray(keys[i])] = 1
        elif (checkWin(getBoard(getStringFromArray(keys[i])), 2 - (player + 1) % 2)):
            table[getStringFromArray(keys[i])] = -1
        elif (isFull(getStringFromArray(keys[i]))):
            table[getStringFromArray(keys[i])] = -0.5
        else:
            table[getStringFromArray(keys[i])] = 0
    return table



def getStringFromArray(array):
    out = ""
    for i in range(len(array)):
        out += str(array[i])
    return out

def getBoardString(board):
    out = ""
    for i in range(3):
        for j in range(3):
            out += str(board[i][j])
    return out

def getBoard(string):
    out = [[0, 0, 0],[0, 0, 0],[0, 0, 0]]
    for i in range(9):
        out[i / 3][i % 3] = int(string[i])
    return out


def checkWin(board, playerNum):
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

def getNeighborStates(state, player):
    out = {}
    for i in range(9):
        if (state[i] == '0'):
            tmp = state[:i] + str(player) + state[i+1:]
            out[tmp] = [i/3, i%3]
    return out

def updateValues(table, oldState, newState):
    table[oldState] = table[oldState] + stepSize * (table[newState] - table[oldState])

def getBestMove(table, board, player):
    state = getBoardString(board)
    nextStates = getNeighborStates(state, player)
    maxVal = -5
    nextState = None
    bestMove = None
    for stateString, pos in nextStates.iteritems():
        if (table[stateString] > maxVal):
            maxVal = table[stateString]
            bestMove = pos
            nextState = stateString
    updateValues(table, state, nextState)
    return bestMove
