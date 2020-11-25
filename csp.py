import sudoku
import queue
import random
import util

class SudokuCSP:

    def __init__(self, sudoku):

        self.sudoku = sudoku
        self.initial_board = sudoku.board

        self.variables = []         # A list of cell coordinates
        self.domains = {}           # A dictionary of domains for every variable    
        self.assignments = {}       # A dictionary of assignments (Don't know if necessary just yet)
        
        # List of 27 constraints <scope, relation>
        self.constraints = []   

        
        
        for y in self.initial_board:
            for x in self.initial_board:
                self.variables.append((x,y))        # Put cell from board in variables
                if self.initial_board[y][x] == 0:   # For every variable not already assigned give it default domain 
                    self.domains[(x,y)] = range(1,10)  
                else:                                  # If already assigned give it domain with its value        
                    self.domains[(x,y)] = [self.initial_board[y][x]]


    def backTrackingSearch(self):
        return "Gabagool" # I'm watching Sopranos

    def minConflictSearch(self):
        return "Goomah"

    def ac3Search(self):
        return "Whacked!"

    def humanLikeSearch(self):
        return "Ohhhhh!"

    


        
