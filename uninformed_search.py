import sudoku
import queue
import random
from sudoku import to_string

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

            first_empty = sudoku.next_square(newBoard)

            if first_empty == None:
                continue

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
        '''
        board = self.initial_board
        sudoku = self.sudoku

        frontier = queue.LifoQueue()    # make frontier a stack
        frontier.put(board)

        while not frontier.empty():

            board = frontier.get()

            if sudoku.is_goal(board):
                return board

            
            first_empty = sudoku.next_square(board)

            if first_empty == None:
                continue


            poss_values = list(range(1,10)) #sudoku.get_possible_values(board, first_empty[0], first_empty[1])


            for new_val in poss_values:
                child = sudoku.generate_successor_board(board, first_empty[0], first_empty[1], new_val)

                frontier.put(child)

        return None



