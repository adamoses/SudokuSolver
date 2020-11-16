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

        if sudoku.is_goal(board):
            return board
        
        frontier = queue.Queue()
        frontier.put(board)
        reached = [self.initial_board]

        while not frontier.empty():

            newBoard = frontier.get()

            until_found = True
            x, y = 0, 0

            while until_found:

                if newBoard[y][x] == 0:
                    until_found = False
                    first_empty = (x, y)
                elif x == 8 and y < 8:
                    x = 0
                    y += 1
                elif y == 8 and x == 8:
                    return None
                else:
                    x += 1
                        
            poss_values = sudoku.get_possible_values(newBoard, first_empty[0], first_empty[1])

            for new_val in poss_values:
                child = sudoku.generate_successor_board(newBoard, first_empty[0], first_empty[1], new_val)

                if sudoku.is_goal(child):
                    return child

                if not child in reached:
                    reached.append(child)
                    frontier.put(child)

        return None

    def depthFirst(self):
        board = self.initial_board
        sudoku = self.sudoku

        frontier = queue.LifoQueue()
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



            