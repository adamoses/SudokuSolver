from util import *
import numpy as np
from sudoku import get_possible_values

# Easy difficulty board
board = [[2,4,0,5,6,0,0,9,0],
         [0,6,3,0,9,0,0,2,5],
         [0,0,5,3,0,0,7,6,0],
         [0,1,2,6,0,5,9,4,0],
         [9,0,8,0,0,0,0,0,0],
         [6,0,0,2,0,0,0,5,3],
         [7,0,0,9,0,6,0,0,4],
         [0,0,6,4,7,3,1,0,0],
         [0,0,0,0,0,1,0,7,2]]

domains = {}

# these nester for-loops are just initiliazing the domains
for x in np.arange(0,9):
    for y in np.arange(0,9):
        cell = (x, y)
        if board[y][x] == 0:
            domains[cell] = get_possible_values(board, x, y)
        else:
            domains[cell] = [board[y][x]]


# exhaustively improving the domain until all naked/hidden sets are handled
util = Util()

print(domains)
domains = util.box_reduction(domains)

print(domains)

