# SudokuSolver

This package includes a number of algorithms and approaches to solving template sudoku puzzles.

## Requirements

This package makes use of the following packages:

[numpy](https://numpy.org/install/)
[pygame](https://www.pygame.org/wiki/GettingStarted)

Instructions to install these packages are linked. 

This package also makes use of a number of built-in python modules:

copy, queue, math, timeit, and sys

## Usage

'''
python3 sudoku.py -ALG -g -b BOARD.TXT
'''

**-ALG** can be any one of

    -DFS_uninformed
    -DFS_informed
    -BFS_uninformed
    -BFS_informed
    -CSP_backtrack
    -CSP_backtrack_human

**-g** specifies whether you would like graphics to be displayed as the algorithm computes

**-b** specifies an input file formatted as just a string of numbers read from the puzzle left to right and top to bottom. 0's are to be used to represent blank squares.
