from copy import Error
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
                    self.assignments[(x,y)] = True
                    self.domains[(x,y)] = [self.initial_board[y][x]]

    def checkConstraints(self):
        '''
        Return the num of constraints violated
        '''
        violated = 0

        for constraint in self.constraints:
            scope, relation = constraint
            if not relation(scope):
                violated += 1
        
        return violated

    def backTrackingSearch(self):
        '''
        Alot to do in this function still. Think we're going to run into problems with using self instead of a 
        physical copy of a csp object. Still, working around it.
        '''
        assignments = self.assignments
        board = self.initial_board
        
        def selectUnassigned(self, assignment):
            '''
            Select a cell that hasn't been assigned, with the smallest domain

            Returns: A cell
            '''
            assigned = [k for k,v in iter(assignments.items())]  # a list of assigned 
            unassigned = list(set(self.variables) - set(assigned))
            
            if not len(unassigned):
                raise Exception('Didnt return when goal state was found')

            min_remaining_vals = unassigned[0]
            for uc in unassigned:
                if len(self.domains[uc]) < len(self.domains[min_remaining_vals]):
                    min_remaining_vals = uc

            return min_remaining_vals

        def orderDomainValues(var, assignment):
            
            return "b"

        def backtrack(assignment):
            if assignment.isGoal(): 
                return assignment
            var = selectUnassigned(assignment)   # a cell
            x, y = var
            ordered_vals = orderDomainValues(var,assignment)    # domain of cell ordered 
            for val in ordered_vals:
                if not self.checkConstraints(val): 
                    prev = assignment[y][x]
                    assignment[y][x] = val
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

    


        
