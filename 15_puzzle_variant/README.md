# Artificial-Intelligence-15puzzle_variant
* Design and Implementation of a program that finds a solution to the 15 Puzzle variant problem using A* (A-Star) Search algorithm.
* The program finds the shortest possible moves to restore canonical configuration given initial board configuration.
* Designed and tested various heuristic functions to find the best heuristic function of A* search.

Variant of the 15-puzzle: when the empty tile is on the edge of the board, the tile on the opposite side of the board can be slid into the opening.

## Running the tests
python puzzle.py [input-board-filename]
where input-board-filename is a text file containing a board configuration in a format like:
5 7 8 1
10 2 4 3
6 9 11 12
15 13 14 0
where 0 is the position of the empty tile.
