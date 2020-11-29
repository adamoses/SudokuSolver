from copy import Error, deepcopy
import queue
import random
from util import *

class CSP:

    def __init__(self, sudoku):
        util = Util()
        self.sudoku = sudoku
        self.initial_board = sudoku.board

        self.variables = {}         # A dictionary of cell coordinates
        self.domains = {}           # A dictionary of domains for every variable    
        self.constraints = []       # List of 27 constraints <scope, relation>
        
        for y in range(0,9):
            t_row = util.abstractRow(y)
            t_col = util.abstractCol(y)
            t_box = util.abstractBox(y)
            self.constraints.append((t_row,util.allDiff))
            self.constraints.append((t_col,util.allDiff))
            self.constraints.append((t_box,util.allDiff)) 
            for x in range(0,9):
                if self.initial_board[y][x] == 0:   # For every variable not already assigned give it default domain 
                    self.domains[(x,y)] = range(1,10)  
                    self.variables[(x,y)] = False       # Put cell from board in variables  
                else:                                  # If already assigned give it domain with its value 
                    self.domains[(x,y)] = [self.initial_board[y][x]]
                    self.variables[(x,y)] = True
    
    def checkConstraints(self,assignment):
        for constraint in self.constraints:
            scope,relation = constraint
            if not relation(self,scope):
                return False
        return True



class BackTrackingSearch:

    def __init__(self, csp):
        self.initial_csp = csp
        self.assignment = csp.initial_board.copy()
        self.sudoku = csp.sudoku
    
    def selectVar(self,csp,assignment):
        '''
        Eventually implement mrv and degree heuristic
        '''
        unassigned = [k for k,v in iter(csp.variables.items()) if not v]
        return unassigned[0]

    def orderValues(self,csp,var,assignment):
        '''
        Eventually implement lcv
        Returns: A list of values in domain of var
        '''
        return csp.domains[var]

    def backtrack(self, csp, assignment):
        if self.sudoku.is_goal(assignment): # if board has properly been assigned, return
            return assignment
        
        var = self.selectVar(csp, assignment) # select a cell with minimum remaining values in domain
        x, y = var
        values = self.orderValues(csp, var, assignment) # order vals by least constraining
        for value in values:
            # check if value works on board
            new_assignment = assignment.copy()
            new_assignment[y][x] = value
            new_csp = csp
            new_csp.variables[(var)] = True
            if new_csp.checkConstraints(new_assignment):
                result = self.backtrack(new_csp,new_assignment)
                if result is not None:
                    return result

        return None



    def search(self):
        return self.backtrack(self.initial_csp, self.assignment.copy())
        
    

