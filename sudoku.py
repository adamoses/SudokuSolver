from csp import *
import math
import numpy as np
from copy import deepcopy
import random
from uninformed_search import *
import sys
import util

class Sudoku:

    def __init__(self, board, show_graphics = True):

        self.show_graphics = show_graphics
        self.board = board

        print(self.to_string(board))  


        # initializing pygame and pygame windows
        if self.show_graphics:
            import pygame
            pygame.init()
            done = False
            self.shape = (self.WIDTH, self.HEIGHT) = (500,500)
            self.window  = pygame.display.set_mode(size=self.shape, flags= pygame.RESIZABLE | pygame.SHOWN)

            WHITE = (255, 255, 255)
            self.render_board(self.board)

        uninformed = UninformedSearch(self)

        csp = CSP(self)
        backtracking = BackTrackingSearch(csp)
        self.board = backtracking.search()
        
        #self.board = uninformed.get_solution(uninformed.depthFirst)

        if self.board is not None:
            print(self.to_string(self.board))
        else:
            print("Couldn't find a solution")
            sys.exit()

        if self.show_graphics:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: sys.exit()

                self.render_board(self.board)

        

    def draw_grid(self):

        import pygame

        BLACK = [0,0,0]
        WHITE = [255,255,255]

        self.window.fill(WHITE)

        # draw the outside border
        pygame.draw.rect(self.window, BLACK, pygame.Rect(25, 25, self.WIDTH-50, self.HEIGHT-50), 5)

        # draw the 9 boxes
        pygame.draw.rect(self.window, BLACK, pygame.Rect(25, 25, 150, 150), 5)
        pygame.draw.rect(self.window, BLACK, pygame.Rect(25, 175, 150, 150), 5)
        pygame.draw.rect(self.window, BLACK, pygame.Rect(25, 325, 150, 150), 5)
        pygame.draw.rect(self.window, BLACK, pygame.Rect(175, 25, 150, 150), 5)
        pygame.draw.rect(self.window, BLACK, pygame.Rect(175, 175, 150, 150), 5)
        pygame.draw.rect(self.window, BLACK, pygame.Rect(175, 325, 150, 150), 5)
        pygame.draw.rect(self.window, BLACK, pygame.Rect(325, 25, 150, 150), 5)
        pygame.draw.rect(self.window, BLACK, pygame.Rect(325, 175, 150, 150), 5)
        pygame.draw.rect(self.window, BLACK, pygame.Rect(325, 325, 150, 150), 5)

        # draw row lines
        pygame.draw.line(self.window, BLACK, (25, 75), (475, 75), 2)
        pygame.draw.line(self.window, BLACK, (25, 125), (475, 125), 2)
        pygame.draw.line(self.window, BLACK, (25, 225), (475, 225), 2)
        pygame.draw.line(self.window, BLACK, (25, 275), (475, 275), 2)
        pygame.draw.line(self.window, BLACK, (25, 375), (475, 375), 2)
        pygame.draw.line(self.window, BLACK, (25, 425), (475, 425), 2)

        # draw col lines
        pygame.draw.line(self.window, BLACK, (75, 25), (75, 475), 2)
        pygame.draw.line(self.window, BLACK, (125, 25), (125, 475), 2)
        pygame.draw.line(self.window, BLACK, (225, 25), (225, 475), 2)
        pygame.draw.line(self.window, BLACK, (275, 25), (275, 475), 2)
        pygame.draw.line(self.window, BLACK, (375, 25), (375, 475), 2)
        pygame.draw.line(self.window, BLACK, (425, 25), (425, 475), 2)

    def render_board(self, board):

        import pygame

        self.draw_grid()

        BLACK = [0,0,0]

        # for each cell
        for x in range(9):
            for y in range(9):

                # if it isn't blank
                if not board[x][y] == 0:

                    # create number and place it on the window
                    font = pygame.font.SysFont('arial', 40)
                    num = font.render(str(board[x][y]), True, BLACK)
                    self.window.blit(num, (40+y*50, 25+x*50))

        pygame.display.flip()


    def generate_successor_board(self, board, x, y, val):

        WHITE = (255, 255, 255)
        new_board = deepcopy(board)
        new_board[y][x] = val

        if self.show_graphics:
            self.render_board(new_board)
        
        return new_board




    def get_possible_values(self, board, x, y):

        # start with all the values possible
        possible_vals = set(range(1,10))

        # determine which box we are in 
        boxx, boxy = (math.floor(x/3), math.floor(y/3))

        # determine which values are in the same row
        in_row = set([i for i in board[y]])

        # determine which values are in the same column
        in_col = set([i for i in [board[j][x] for j in range(9)]])

        # determine which values are in the same box
        in_box = set(np.array([i for i in [board[j][boxx*3: boxx*3+3] for j in range(boxy*3,boxy*3+3)]]).flatten())
        
        # take the union of all those 
        not_possible = in_row.union(in_col, in_box)

        # and the possible values are those that remain
        possible_vals = possible_vals.difference(not_possible)

        return list(possible_vals)


    def is_goal(self, board):

        for x in range(9):
            for y in range(9):

                value = board[y][x]

                boxx, boxy = (math.floor(x/3), math.floor(y/3))

                # determine which values are in the same row
                row = list([i for i in board[y]])

                # determine which values are in the same column
                col = list([i for i in [board[j][x] for j in range(9)]])

                # determine which values are in the same box
                box = list(np.array([i for i in [board[j][boxx*3: boxx*3+3] for j in range(boxy*3,boxy*3+3)]]).flatten())

                if row.count(value) > 1 or col.count(value) > 1 or box.count(value) > 1 or value == 0:
                    return False

        return True

    def to_string(self, board):

        string = ''

        horizontal = '--------+-------+--------\n'

        for y in range(0,9):
            for x in range(0,9):
                
                if x == 3 or x == 6:
                    string += '| ' + str(board[y][x]) + ' '
                elif x == 8:
                    string += str(board[y][x]) + ' |\n'
                elif x == 0 and (y == 3 or y == 6):
                    string += horizontal + '| ' + str(board[y][x]) + ' '
                elif x == 0:
                    string += '| ' + str(board[y][x]) + ' '
                else:
                    string += str(board[y][x]) + ' '
                
        return  string
    
    def getRow(self, index):
        '''
        Returns a list of 9 cell values following:

        [valAt(index,0), valAt(index,1), ... , valAt(index,8)]
        '''
        row = []
        for i in range(0,9):
            row.append(self.board[index][i])
        
        return row

    def getCol(self, index):
        '''
        Returns a list of 9 cell values following:

        [valAt(0,index), valAt(1,index), ... , valAt(8,index)]
        '''
        col = []
        for i in range(0,9):
            col.append(self.board[i][index])

        return col

    def getBox(self, index):
        '''
        Returns a list of 9 cell values which are the values
        at the box index according to : 

        0 | 1 | 2
        _ | _ | _
        3 | 4 | 5
        _ | _ | _
        6 | 7 | 8
        
        '''
        box = []
        coords = util.box_dictionary[index]

        for i in range(0,9):
            x,y = coords[i]
            box.append(self.board[y][x])

        return box
                
                





if __name__ == "__main__":


    # The following chunk of code comes from https://www.kaggle.com/bryanpark/sudoku
    # It loads a million sudoku games into matrices conveniently formatted

    # import numpy as np
    # quizzes = np.zeros((1000000, 81), np.int32)
    # solutions = np.zeros((1000000, 81), np.int32)
    # for i, line in enumerate(open('sudoku.csv', 'r').read().splitlines()[1:]):
    #     quiz, solution = line.split(",")
    #     for j, q_s in enumerate(zip(quiz, solution)):
    #         q, s = q_s
    #         quizzes[i, j] = q
    #         solutions[i, j] = s
    # quizzes = quizzes.reshape((-1, 9, 9))
    # solutions = solutions.reshape((-1, 9, 9))

    # board = quizzes[random.randint(1,999999)].tolist()

    board = np.zeros(shape=(9,9), dtype=int).tolist()


    s = Sudoku(board, show_graphics=True)