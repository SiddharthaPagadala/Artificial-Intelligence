# n_rooks_queens.py : Solve the N-Rooks and N-Queens problem!
#
# The N-rooks problem is: Given an empty NxN chessboard, place N rooks on the board so that no rooks
# can take any other, i.e. such that no two rooks share the same row or column.

# Siddhartha Pagadala, September 2016
# The N-Queens Problem is:Given an empty NxN chessboard, place N Queens on the board so that no Queens
# can take any other, i.e. such that no two Queens share the same row or column or diagonal.

# This is N, the size of the board.
N=27

# Count # of pieces in given row
def count_on_row(board, row):
    return sum( board[row] ) 

# Count # of pieces in given column
def count_on_col(board, col):
    return sum( [ row[col] for row in board ] ) 

# Count total # of pieces on board
def count_pieces(board):
    return sum([ sum(row) for row in board ] )

# Return a string with the board rendered in a human-friendly format
def printable_board(board):
    return "\n".join([ " ".join([ "Q" if col else "_" for col in row ]) for row in board])

# Add a piece to the board at the given position, and return a new board (doesn't change original)
def add_piece(board, row, col):
    return board[0:row] + [board[row][0:col] + [1,] + board[row][col+1:]] + board[row+1:]

# Get list of successors of given board state
def successors(board):
    return [ add_piece(board, r, c) for r in range(0, N) for c in range(0,N) ]

#Get list of successors of given board state which fixes adding N+1 rooks and not adding any rook
def successors2(board):
    board_count =  count_pieces(board)
    return [ add_piece(board, r, c) for r in range(0, N) for c in range(0,N) if board[r][c]==0 and board_count!=N ]

#Get list of successors which places rook in left most empty column without any conflict with existing board elements(not in same row and column)
def successors3(board):
    left_most_empty_col = count_pieces(board)
    row_conflict = [board.index(row) if 1 in row else N+1 for row in board]
    return [add_piece(board, r, left_most_empty_col) for r in range(0,N) if r not in row_conflict]

# Checks for given row and column whether diagonal conflict occurs and can place an element. If it is not valid to place return False else True
def nqueens_check_diag(board,row,column):
        x = 1
        bool = True
        for c in range(column-1,-1,-1):
                if row+x<N:
                        if board[row+x][c] == 1:
                                bool= False
                                return False
                        else:
                                x = x+1
        x=1
        if bool:
                for c in range(column-1,-1,-1):
                        if row-x>=0:
                                if board[row-x][c] == 1:
                                        bool= False
                                        return False
                                else:
                                        x = x+1
                return True


#Get list of successors which places queen in left most empty column without any conflict with existing board elements(not in same row,column and diagonal)
def nqueens_successors(board):
        left_most_empty_col = count_pieces(board)
        row_conflict = [board.index(row) if 1 in row else N+1 for row in board]
        c = [add_piece(board, r, left_most_empty_col) for r in range(0,N) if r not in row_conflict if nqueens_check_diag(board,r,left_most_empty_col)]
        return c

# check if board is a goal state
def is_goal(board):
    return count_pieces(board) == N and \
        all( [ count_on_row(board, r) <= 1 for r in range(0, N) ] ) and \
        all( [ count_on_col(board, c) <= 1 for c in range(0, N) ] )

# Solve n-rooks!
def solve(initial_board):
    fringe = [initial_board]
    while len(fringe) > 0:
        for s in successors3( fringe.pop() ):
            if is_goal(s):
                return(s)
            fringe.append(s)
    return False

#solve n-queens
def nqueens_solve(initial_board):
    fringe = [initial_board]
    while len(fringe) > 0:
        for s in nqueens_successors( fringe.pop() ):
            if is_goal(s):
                return(s)
            fringe.append(s)
    return False


# The board is stored as a list-of-lists. Each inner list is a row of the board.
# A zero in a given square indicates no piece, and a 1 indicates a piece.
initial_board = [[0]*N]*N
print "Starting from initial board:\n" + printable_board(initial_board) + "\n\nLooking for solution of N rooks...\n"
solution = solve(initial_board)
print "Looking for solution of N queens...\n"
nqueens_solution = nqueens_solve(initial_board)
print " Nrooks solution:\n"
print printable_board(solution) if solution else "Sorry, no solution found for N rooks. :("

print "Nqueens solution:\n"
print printable_board(nqueens_solution) if solution else "Sorry, no solution found for Nqueens. :("

