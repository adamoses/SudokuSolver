import sudoku
import queue
import random

class UninformedSearch:

    def __init__(self, sudoku):

        self.sudoku = sudoku
        self.initial_board = sudoku.board

    def get_solution(self, func):

        return func()


    def breadthFirst(self):

        board = self.initial_board           
        sudoku = self.sudoku                 

        if sudoku.is_goal(board):           # if initial board is goal, return
            return board
        
        frontier = queue.Queue()            # frontier is queue in BFS
        frontier.put(board)                 # put initial board on queue
        reached = [self.initial_board]      # mark as reached

        while not frontier.empty():         # while frontier is not empty

            newBoard = frontier.get()       # explore first board put on queue

            until_found = True              
            x, y = 0, 0                     # init counter to top left cell

            while until_found:      # populate board one cell at a time

                if newBoard[y][x] == 0:     # if cell is empty 
                    until_found = False         # break loop
                    first_empty = (x, y)        # mark location of empty cell          
                elif x == 8 and y < 8:      # if at end of a row 
                    x = 0                       # reset row pointer 
                    y += 1                      # inc col
                elif y == 8 and x == 8:     # if at end of the board 
                    return None                 # then finished
                else:
                    x += 1                  # else move to next cell in row
                        
            # get list of possible values for a cell
            poss_values = sudoku.get_possible_values(newBoard, first_empty[0], first_empty[1])

            # for each possible value
            for new_val in poss_values:
                # generate a new board with the new cell val at empty 
                child = sudoku.generate_successor_board(newBoard, first_empty[0], first_empty[1], new_val)

                if sudoku.is_goal(child):   # if goal, return
                    return child

                if not child in reached:    # if this iteration hasnt been reached
                    reached.append(child)   # mark as reached 
                    frontier.put(child)     # push to frontier

        return None

    def depthFirst(self):
        '''
        Reference breadth-first for near identical deocumentation
        
        FOR ADAM******* do we need a reached list in breadth-first? // will there be times we expand the same 
                        state twice ? 
        '''
        board = self.initial_board
        sudoku = self.sudoku

        frontier = queue.LifoQueue()    # make frontier a stack
        frontier.put(board)

        while not frontier.empty():

            board = frontier.get()

            if sudoku.is_goal(board):
                return board

            until_found = True
            x,y = 0,0 

            while until_found:

                if board[y][x] == 0:
                    until_found = False
                    first_empty = (x, y)
                elif x == 8 and y < 8:
                    x = 0
                    y += 1
                elif y == 8 and x == 8:
                    print(board)
                    return None
                else:
                    x += 1

            poss_values = sudoku.get_possible_values(board, first_empty[0], first_empty[1])


            for new_val in poss_values:
                child = sudoku.generate_successor_board(board, first_empty[0], first_empty[1], new_val)

                frontier.put(child)

        return None

