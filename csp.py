from copy import Error, deepcopy
import math
import queue
import random
from util import *
import timeit

class CSP:

    def __init__(self, sudoku):
        util = Util()
        self.sudoku = sudoku
        self.initial_board = sudoku.board

        self.variables = {}         # A dictionary of cell coordinates
        self.domains = {}           # A dictionary of domains for every variable
        
        for x in range(0,9): 
            for y in range(0,9):
                if self.initial_board[x][y] == 0:   # For every variable not already assigned give it default domain 
                    self.domains[(x,y)] = [*range(1,10)]  
                    self.variables[(x,y)] = False       # Put cell from board in variables  
                else:                                  # If already assigned give it domain with its value 
                    self.domains[(x,y)] = [self.initial_board[x][y]]
                    self.variables[(x,y)] = True
        
        for var, b in self.variables.items():
            if b:
                x,y = var
                util.refactorDomains(self.initial_board[x][y],(x,y),self.domains)

    
    def checkConstraints(self,assignment):
        for constraint in self.constraints:
            scope,relation = constraint
            if not relation(self,scope):
                return False
        return True



class BackTrackingSearch:

    def __init__(self, csp, graphics = False, human=False):
        self.csp = csp
        self.assignment = deepcopy(csp.initial_board)
        self.domains = deepcopy(csp.domains)
        self.sudoku = csp.sudoku
        self.cells_expanded = 0
        self.graphics = graphics
        self.util = Util(human=human)

        self.time = None
    
    def selectVar(self,domains,assignment):
        '''
        Selects variable by the MRV heuristic.
        '''
        pq = queue.PriorityQueue()  # order by length of domain

        for x in range(9):
            for y in range(9):
                if assignment[x][y] == 0:
                    pq.put((len(domains[(x,y)]),(x, y))) 
        
        output = pq.get()   # get the cell with fewest remaining options
        return output[1]

    def orderValues(self,var,domains):
        '''
        Eventually implement lcv
        Returns: A list of values in domain of var
        '''
        return domains[var]
    
    def backtrack(self, domains, assignment):
        '''
        Recursive algorithm that keeps track of cell domains and assignments and makes sudoku moves
        based on what is possible. 
        '''
        if self.sudoku.is_goal(assignment): # if board has properly been assigned, return
            return assignment
        
        self.cells_expanded += 1
        var = self.selectVar(domains, assignment) # select next unassigned cell
        x, y = var
        possible_values = self.orderValues(var, domains) # get a list of possible values from domain
        for value in possible_values:
            new_assignment = deepcopy(assignment)
            new_assignment[x][y] = value            # assign val from left over domain
            new_domains = deepcopy(domains)             
            new_domains[var] = [value]
            
            self.util.refactorDomains(value,var,new_domains) # restructure all affected domains
            

            if self.graphics:
                self.sudoku.render_board(new_assignment)

            result = self.backtrack(new_domains,new_assignment)
            if result is not None:
                return result

        return None

    def search(self):
        '''
        Wrapper function for backtracking search that record the time and number of nodes expanded.
        '''
        start = timeit.default_timer() 
        output = self.backtrack(self.domains, self.assignment)
        end = timeit.default_timer()

        self.time = end-start

        print("Cells expanded: ", self.cells_expanded)
        print ("Time: ", end - start , "\n")
        print ("Output: ")
        return output
    

