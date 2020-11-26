import sudoku
import queue
import random
import util

class SudokuCSP:

    def __init__(self, sudoku):

        self.sudoku = sudoku
        self.initial_board = sudoku.board

        self.variables = []         # A list of cell coordinates
        self.arcs = queue.Queue()
        self.domains = {}           # A dictionary of domains for every variable    
        self.assignments = {}       # A dictionary of assignments 
        
        # List of 27 constraints <scope, relation>
        self.constraints = []   

        for y in self.initial_board:
            t_row = self.sudoku.getRow(y)
            t_col = self.sudoku.getCol(y)
            t_box = self.sudoku.getBox(y)
            self.constraints.append((t_row,util.allDiff))
            self.constraints.append((t_col,util.allDiff))
            self.constraints.append((t_box,util.allDiff)) 
            for x in self.initial_board:
                self.variables.append((x,y))        # Put cell from board in variables
                if self.initial_board[y][x] == 0:   # For every variable not already assigned give it default domain 
                    self.domains[(x,y)] = range(1,10)  
                else:                                  # If already assigned give it domain with its value        
                    self.domains[(x,y)] = [self.initial_board[y][x]]

    def checkConstraints():
        '''
        Return the num of constraints violated
        '''
        return 0

    def backTrackingSearch(self):
        '''
        Alot to do in this function still. Think we're going to run into problems with using self instead of a 
        physical copy of a csp object. Still, working around it.
        '''
        assignments = self.assignments
        board = self.initial_board
        
        def selectUnassigned(assignment):
            return "a"

        def orderDomainValues(var, assignment):
            return "b"

        def inference(var, assignment):
            return "c"

        def backtrack(assignment):
            if assignment.isGoal(): 
                return assignment
            var = selectUnassigned(assignment)
            x, y = var
            ordered_vals = orderDomainValues(var,assignment)
            for val in ordered_vals:
                if not self.checkConstraints(val): # this also doesnt work (pseudocode)
                    prev = assignment[y][x]
                    assignment[y][x] = val
                    inferences = inference(var,assignment)
                    if inferences: # if inferences were correct (forward checking)
                        new_domain = self.domains
                        new_domain[var] = [val]

                        result = backtrack(assignment.copy()) 
                        if result is not None:
                            return result
                        
                    assignment[y][x] = prev  # reset asssignment if it didnt work 
                    
            return None

        return backtrack(board.copy())

    def minConflictSearch(self):
        return "Goomah"

    def humanLikeSearch(self):
        return "Ohhhhh!"

    


        
