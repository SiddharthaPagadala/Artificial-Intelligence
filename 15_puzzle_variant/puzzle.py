import copy
import heapq
import sys

####Implemented two heuristic functions:
#### one is number of misplaced tiles
####other is modified version of manhattan distance by considering the movement of tiles across edge
####Both heuristic functions are admissible and consistent
####But second heuristic with modified manhattan distance finds solution much faster than the first one

#Priority Queue implementation using heapq
class PriorityQueue:
	def __init__(self):
		self._queue = []
        # insert priority to -priority can change to max priority queue
	def push(self, item, priority):
		heapq.heappush(self._queue, (priority, item))
	def pop(self):
		return heapq.heappop(self._queue)[1]
	def empty(self):
		return len(self._queue)==0

#Reads initial state from file
def read_data(file):
	f = open(file, 'r')
	initial_board = [ [int(s) for s in line.strip('\n').split(' ')] for line in f.readlines() ]
	f.close()
	return initial_board

# Return a string with the board rendered in a human-friendly format
def printable_board(board):
    return "\n".join([ " ".join([ str(col) for col in row ]) for row in board])

#Returns a string with desired output format of moves direction of empty tile
def print_board_moves(moves):
	return " ".join(moves)

#Number of misplaced tiles
def heuristic(board): 
	goal_state = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]]
	return 16-len([l for i,j in zip(board,goal_state) for l,m in zip(i,j) if l==m])


#Modified manhattan distance by considering edge movement
def heuristic_manhattan(board):
	goal_state = {1:(0,0),2:(0,1),3:(0,2),4:(0,3),5:(1,0),6:(1,1),7:(1,2),8:(1,3),9:(2,0),10:(2,1),11:(2,2),12:(2,3),13:(3,0),14:(3,1),15:(3,2)}
	man_dist = []
	for r in board:
		for c in r:
			if c in goal_state.keys():
				if abs(goal_state[c][0] - board.index(r)) == 3:
					row_manh = 1
				else:
					row_manh = abs(goal_state[c][0] - board.index(r))
				if abs(goal_state[c][1] - r.index(c)) == 3:
					col_manh = 1
				else:
					col_manh = abs(goal_state[c][1] - r.index(c))
				man_dist.append(row_manh + col_manh)

	return sum(man_dist)

#to check whether goal state is reached
def is_goal(board):
	goal_state = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]]
	return board == goal_state

#returns row and column	of empty tile
def get_empty_tile(board):
	row_col = [(board.index(row),row.index(0)) for row in board if 0 in row]
	return row_col[0][0],row_col[0][1]

#moves empty tile to position given by row,col attributes
def move_empty_tile(board,row,col,row_empty_tile,col_empty_tile):
	board1=copy.deepcopy(board)
	board1[row_empty_tile][col_empty_tile]=board1[row][col]
	board1[row][col] = 0
	return board1

#successors of the board
def successors(board):
	row_empty_tile,col_empty_tile = get_empty_tile(board)
	#gets all possible moves for moving empty tile
	l = [(0 if r >3 else 3 if r <0 else r,0 if c >3 else 3 if c < 0 else c) for (r,c) in [(row_empty_tile,col_empty_tile-1),(row_empty_tile,col_empty_tile+1),(row_empty_tile-1,col_empty_tile),(row_empty_tile+1,col_empty_tile)]]
	succ = []
	return [  move_empty_tile(board,x[0],x[1],row_empty_tile,col_empty_tile) for x in l]

#converts list to tuple for using it as dict key
def list_to_tuple(list):
	return tuple([tuple(x) for x in list])

#finds the solution
#cost function = parent_state cost+1
#parent dictionary to construct path
def solve(initial_board):
	fringe = PriorityQueue()
	fringe.push(initial_board,0)
	cost = {}
	cost[list_to_tuple(initial_board)] = 0
	parent={}
	parent[list_to_tuple(initial_board)] = None
	while not fringe.empty():
		state = fringe.pop()
		if is_goal(state):
			return state,parent
		for s in successors(state):
			new_cost = cost[list_to_tuple(state)] + 1
			if list_to_tuple(s) not in cost or new_cost < cost[list_to_tuple(s)]:
				cost[list_to_tuple(s)] = new_cost
				priority = new_cost + heuristic_manhattan(s)
				fringe.push(s,priority)
				parent[list_to_tuple(s)] = state
	return False

#gives direction of empty tile movement
def get_move_direction(parent_state,succ_state):
	row1,col1 = get_empty_tile(parent_state)
	row2,col2 = get_empty_tile(succ_state)
	if row1 == row2:
		if col2-col1 >0 or col2-col1 == -3:
			if col2-col1>1:
				return 'L'
			else:
				return 'R'
		else:
			return 'L'
	elif col1 == col2:
		if row2-row1 >0 or row2-row1 == -3:
			if row2-row1>1:
				return 'U'
			else:
				return 'D'
		else:
			return 'U'

#constructs path of sequence of moves from initial state to goal state
def construct_path(path, initial_board, goal):
	state = goal
	moves_state = [state]
	moves=[]
	while state != initial_board:
		moves.append(get_move_direction(path[list_to_tuple(state)],state))
		state = path[list_to_tuple(state)]
		moves_state.append(state)

	moves_state.reverse()
	moves.reverse()
	return moves_state, moves



#Intial board is taken as list of rows with 0 as empty tile
#input_file = sys.argv[1]
#initial_board = read_data(input_file)
initial_board = [[5,7,8,1],[10,2,4,3],[6,9,11,12],[15,13,14,0]]
print("Initial Board")
print(printable_board(initial_board))
print("\n\nLooking for solution of 15 puzzle...\n")

solution,path = solve(initial_board)
print("Solution")
print(printable_board(solution))
goal_state = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]]

moves_state,moves = construct_path(path,initial_board,goal_state)
print("\nMoves direction:\n")
print(print_board_moves(moves))



