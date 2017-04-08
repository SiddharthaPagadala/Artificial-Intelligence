import sys
import copy
from timeit import default_timer as timer

class state:
    def __init__(self, depth=None, alpha=None, beta=None, evaluation=None,board=None,successor=None,parent=None):
        self.depth = depth
        self.alpha = alpha
        self.beta = beta
        self.evaluation = evaluation
        self.board = board
        self.successors = successor
        self.parent = parent

    # returns successor of given state by placing marble(w or b) in empty spot
    def successors_cal(self, marble, n):
        board = copy.deepcopy(self.board)
        succ_States = [add_piece(board, r, c, marble) for r in range(0, n) for c in range(0, n) if board[r][c] == '.']

        for s in succ_States:
            succ_States = dupRemoval(s, succ_States)
        self.successors = [state(board=d) for d in succ_States]
#returns which marble color to place in next move
def getMarbleColor(initial_board):
    whiteCount = getMarbleCountRow(initial_board,'w')
    blackCount = getMarbleCountRow(initial_board,'b')

    if whiteCount == blackCount or whiteCount < blackCount or (whiteCount == 0 and blackCount == 0):
        return 'w'
    else:
        return 'b'

def getMarbleCountRow(board,c):
    return sum([1 if m==c else 0 for row in board for m in row ])

def getIndexMarble(list1,c,n):
    return [ind if elem==c else n+1 for ind,elem in enumerate(list1) ]

def emptyReplace(list1,j):
    return [j if elem == '.' else elem for elem in list1]

#Determines whether given row, column, diagonal is favourable for max player and min player
#returns True if favourable
def getFavPlayer(list1,n,k,maxPlayerMarble,minPlayerMarble):
    list1Complete = [[j if elem=='.' else elem for i,elem in enumerate(list1) ] for j in [maxPlayerMarble,minPlayerMarble]]
    retFavPlayer= [any([j] * k == r[i:i + k] for i in range(len(r) - 1)) for r in list1Complete for j in [maxPlayerMarble,minPlayerMarble]][::3]
    return retFavPlayer


#checks for open column
def getRowCheck(state,maxPlayerMarble,minPlayerMarble):
    stateComplete=[[[j if elem == '.' else elem for i, elem in enumerate(l1)] for l1 in state] for j in [maxPlayerMarble, minPlayerMarble]]
    rowCheck = [[any([j] * k == row[rkInd:rkInd + k] for rkInd in range(n - k + 1)) for row in scomp] for rowInd, scomp in enumerate(stateComplete) for j in [maxPlayerMarble, minPlayerMarble]][::3]
    return [sum(elem) for elem in rowCheck]

#checks for open row
def getColCheck(state,maxPlayerMarble,minPlayerMarble):
    listComplete = [list(elem) for elem in zip(*state)]
    stateComplete = [[[j if elem == '.' else elem for i, elem in enumerate(l1)] for l1 in listComplete] for j in [maxPlayerMarble, minPlayerMarble]]
    colCheck = [[any([j] * k == row[rkInd:rkInd + k] for rkInd in range(n - k + 1)) for row in scomp] for rowInd, scomp in enumerate(stateComplete) for j in [maxPlayerMarble, minPlayerMarble]][::3]
    return [sum(elem) for elem in colCheck]

#Gets complete diagonal elements
#source:stack overflow
def diagonal(l):

    L = copy.deepcopy(l)
    return_list = [[] for i in range(len(L))]

    for line in range(len(L)):
        L[line].reverse()
        i = line

        for elem in L[line]:
            if i >= len(return_list):
                return_list.append([])

            return_list[i].append(elem)
            i += 1

    return_list.reverse()
    return return_list

def getDiagCheck(state,maxPlayerMarble,minPlayerMarble):
    diag = diagonal(state)
    cw_90 = [list(elem) for elem in list(reversed(zip(*state)))]
    diag1 = diagonal(cw_90)

    favPlayer = [getFavPlayer(list1, n, k, maxPlayerMarble, minPlayerMarble) for list1 in diag+diag1]
    maxPlayerFavCount = sum([1 if f[0] == True else 0 for f in favPlayer])
    minPlayerFavCount = sum([1 if f[1] == True else 0 for f in favPlayer])
    return [maxPlayerFavCount,minPlayerFavCount]
#returns all the column elements of the given board state
def getColElem(board,n):
    return [list(elem) for elem in zip(*board)]


#returns all the diagonal elements of the given board state
def getDiagElem(board,n):
    return [[r[i] if j == 0 else r[len(r) - 1 - i] for i, r in enumerate(board)] for j in [0, 1]]

#Evaluation Function
#Evaluation Function = number of rows, columns, diagonals open for min player - number of rows, columns, diagonals open for max player
#Calculates evaluation function for the given state and
#returns the value
def evaluationFunction(board,n,k,maxPlayerMarble,minPlayerMarble):
    r1 = getRowCheck(board,maxPlayerMarble,minPlayerMarble)
    c1 = getColCheck(board,maxPlayerMarble,minPlayerMarble)
    d1 = getDiagCheck(board,maxPlayerMarble,minPlayerMarble)
    openCount=[r1[0]+ c1[0] + d1[0],r1[1]+ c1[1] + d1[1]]

    goalCheck = isGoalState(board,n,k,maxPlayerMarble,minPlayerMarble)
    if goalCheck[1][0]:
        if getMarbleColor(board) == minPlayerMarble:
            if goalCheck[1][0] == True:
                return(openCount[1]-openCount[0]-k)
        else:
           return(openCount[1] - openCount[0]+k)
    else:
        return(openCount[1]-openCount[0])

#adds marble(w or b) at given position(row,col) in board
def add_piece(board, row, col, marble):
    board = board[0:row] + [board[row][0:col] + [marble,] + board[row][col+1:]] + board[row+1:]
    return board



#Check whether state is terminal or goal state: k marbles(w or b) in same row, column, diagonal
def isGoalState(state, n, k,maxPlayerMarble,minPlayerMarble):
    kCombElements = [[e[m:m + k] for e in state[r:r + k]] for m in range(0, n - k + 1) for r in range(0, n - k + 1)]
    colElements = [elem for c in [getColElem(kelem, n) + getDiagElem(kelem, n) + kelem for kelem in kCombElements] for elem in c]

    consecElemCheck = [any([j] * k == r for r in colElements) for j in [maxPlayerMarble, minPlayerMarble]]
    #Checks the board does not contain any empty place
    boardCompleteCheck = [all('.' not in elem for elem in state)]
    return True in consecElemCheck+boardCompleteCheck,consecElemCheck

#Selects maximum alpha of its successor states and updates alpha child alpha is maximum
#returns maximum alpha
def maxValue(state,alpha,beta,depth,n,k,maxPlayerMarble, minPlayerMarble):

    if depth == 0 or isGoalState(state.board,n,k,maxPlayerMarble,minPlayerMarble)[0] :
        state.evaluation = evaluationFunction(state.board,n,k,maxPlayerMarble,minPlayerMarble)
        state.depth = 0
        state.alpha = state.evaluation
        return state.evaluation
    state.successors_cal(maxPlayerMarble,n)
    for s in state.successors:
        alpha = max(alpha,minValue(s,alpha,beta,depth-1,n,k,maxPlayerMarble, minPlayerMarble))
        state.alpha = alpha
        if alpha >= beta:
            return alpha
    return alpha

#Selects minimum beta of its successor states and updates beta child beta is minimum
#returns minimum beta
def minValue(state, alpha, beta, depth, n, k,maxPlayerMarble, minPlayerMarble):
    if depth == 0 or isGoalState(state.board,n,k,maxPlayerMarble,minPlayerMarble)[0] :
        state.evaluation = evaluationFunction(state.board, n, k,maxPlayerMarble,minPlayerMarble)
        state.depth = 0
        state.beta = state.evaluation
        return state.evaluation
    state.successors_cal(minPlayerMarble, n)
    state.depth = depth
    for s in state.successors:
        beta = min(beta, maxValue(s, alpha, beta, depth - 1, n, k, maxPlayerMarble,minPlayerMarble))
        state.beta = beta
        if alpha >= beta:
            return beta
    return beta

#Rotates given states
#and if any rotated state is present in the successors, removes from the successor
#returns the updated successors
def dupRemoval(state,parent):
    for dup in getRotations(state):
        if dup in parent:
            parent.remove(dup)
    return parent

#Performs Alpha Beta Pruning and returns best successor for the given depth and board
def alphaBeta(initialState,depth,n,k,maxPlayerMarble, minPlayerMarble):

    min = state(beta=float("-inf"))
    bList = []

    initialState.alpha = float("-inf")

    initialState.successors_cal(maxPlayerMarble,n)
    #childStates = successors(board,maxPlayerMarble,n)
    for s in initialState.successors:
        b = minValue(s, float("-inf"), float("inf"), depth-1, n, k,maxPlayerMarble, minPlayerMarble)
        bList.append(s)

    for l in bList:
        if l.beta > min.beta:
            min = l
        elif l.beta == min.beta:
            if l.depth > min.depth:
                min = l

    return min

#rotates the given state in counter clockwise in 90, 180, 270 degrees
#returns rotated states
def getRotations(state):
    cw_90 = [list(elem) for elem in list(reversed(zip(*state)))]
    cw_180 = [ list(elem) for elem in list(reversed(zip(*cw_90)))]
    cw_270 = [ list(elem) for elem in list(reversed(zip(*cw_180)))]
    return [cw_90,cw_180,cw_270]

#Transforms given input board to list of lists representation
#list of rows
def generateBoard(board_input,n):
    return [ board_input[i:j] for i,j in [(n*m,n*(m+1)) for m in range(0,n)]]

#prints the board in specified output format
def printBoard(board):
    return ''.join([elem for row in board for elem in row])

#main function
def main():

    initial_board = generateBoard(list(board_input),n)
    initialState = state()
    initialState.board = initial_board
    marbles=['w','b']
    #gets max player marble color
    maxPlayerMarble = getMarbleColor(initial_board)
    marbles.remove(maxPlayerMarble)
    minPlayerMarble = marbles[0]

    #Checks whether input board is terminal state
    if isGoalState(initialState.board,n,k,maxPlayerMarble, minPlayerMarble)[0]:
        print "Already game is over!"
        print "Current board is:"
        print printBoard(initialState.board)
    else:

        IDDFS(initialState,n,k,maxPlayerMarble, minPlayerMarble)

#Performs Iterative Depth Search
def IDDFS(initialState,n,k,maxPlayerMarble, minPlayerMarble):

    for depth in range(1,9999):
        #Alpha Beta Pruning and returns best successor(next move) for max player
        bestSuccessor = alphaBeta(initialState,depth,n,k,maxPlayerMarble, minPlayerMarble)
        print printBoard(bestSuccessor.board)



if __name__ == '__main__':
    start = timer()
    # Input Arguments
    n= int(sys.argv[1])
    k=int(sys.argv[2])
    board_input = sys.argv[3]
    timeLimit = int(sys.argv[4])
    #timeLimit = 1
    #timeThreshold = 3*timeLimit / 4
    #n = 4
    #k = 2
    #board_input = "wbwbw....w.bb..w"
    if len(board_input) > n*n:
        print "Incorrect board, please check length of board"
    else:
        main()
    end = timer()
    #l = [['w', 'b', 'w', 'b'], ['.', '.', '.', '.'], ['w', '.', 'w', '.'], ['.', 'b', '.', 'b']]
    #diag = diagonal(l)
    #print(diag)
    #print(l)
    #favPlayer = [getFavPlayer(list1, 4, 2, 'b', 'w') for list1 in diag]
    #print(favPlayer)
    #print(getDiagCheck(l,'b','w'))
    #print end-start
