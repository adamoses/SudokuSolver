from sudoku import *
import timeit

boards = ['sudoku1.txt', 'sudoku2.txt', 'sudoku3.txt', 'sudoku4.txt', 'sudoku5.txt']
boards = ['test_sudokus/' + b for b in boards]

for b in boards:
    board = np.zeros(81, np.int32)
    string = open(b, 'r').read()
    for index, i in enumerate(string):
        board[index] = i

    board = board.reshape((9, 9))

    Sudoku(board, '-DFS_informed', show_graphics = False)




