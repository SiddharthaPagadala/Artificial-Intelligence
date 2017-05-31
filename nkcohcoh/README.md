# Artificial-Intellegience-nkcohcoh
* Implementation of  two player adversarial game, n-k-coh-coh, a variant of Tic-Tac-Toe game using alpha-beta pruning and minimax algorithms.
* The program recommends next best move to be made given current board state.
* It also displays new state of board after making the recommended move.

## n-k-coh-coh game description: 
n-k-coh-coh is a popular childhood game in a certain rural midwestern town that requires just a board consisting of a grid of n X n squares and some white and black marbles. Initially the board starts empty and all marbles are in a pile beside the board. Player 1 picks up a white marble and places it in any square of the board. Player 2 then picks up a black marble from the pile, and places it in any open square (i.e.any square except the one selected by Player 1). Play continues back and forth, with Player 1 always using white marbles and Player 2 always using black. A player loses the game as soon as they place a marble suchthat there is a continuous line of k marbles of his or her color in the same row, column, or diagonal of the board. (For example, note that 3-3-coh-coh is nearly the same as tic-tac-toe, except that players are trying to avoid completing a row, column or diagonal instead of trying to complete one.)

## Running the Program
python nkcohcoh.py n  time_limit  
n --> board grid shape  
k --> Player loses game if continuous line of k marbles are placed  
board_configutation --> the current state of the board as a string of w's, b's, and .'s, which indicate which squares are filled with a white, black, or no marble, respectively, in row-major order.  
time_limit --> Time limit program should run in seconds

## Program Output
Recommended board state
