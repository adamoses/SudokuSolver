

class Util:

    def __init__(self):
        self.box_dictionary = {
            0 : [(0,0), (0,1), (0,2),
                 (1,0), (1,1), (1,2),
                 (2,0), (2,1), (2,2)],
            1 : [(0,3), (0,4), (0,5),
                 (1,3), (1,4), (1,5),
                 (2,3), (2,4), (2,5)],
            2 : [(0,6), (0,7), (0,8),
                 (1,6), (1,7), (1,8),
                 (2,6), (2,7), (2,8)],
            3 : [(3,0), (3,1), (3,2),
                 (4,0), (4,1), (4,2),
                 (5,0), (5,1), (5,2)],
            4 : [(3,3), (3,4), (3,5),
                 (4,3), (4,4), (4,5),
                 (5,3), (5,4), (5,5)],
            5 : [(3,6), (3,7), (3,8),
                 (4,6), (4,7), (4,8),
                 (5,6), (5,7), (5,8)],
            6 : [(6,0), (6,1), (6,2),
                 (7,0), (7,1), (7,2),
                 (8,0), (8,1), (8,2)],
            7 : [(6,3), (6,4), (6,5),
                 (7,3), (7,4), (7,5),
                 (8,3), (8,4), (8,5)],
            8 : [(6,6), (6,7), (6,8),
                 (7,6), (7,7), (7,8),
                 (8,6), (8,7), (8,8)]
        }
    

    def allDiff(cell_list):
        '''
        Checks if a list of values is all different.

        Returns: A boolean
        '''
        comparison = set(cell_list).intersection(range(1, 10))

        return len(comparison) == 9

    def allDiff1(cell, type_check):
        '''
        Checks if a cell in a <type_check> is comprised of all different values in domain:
                - row = 0
                - col = 1
                - box = 2

        Returns: A boolean
        '''
        ## TODO: Implement if necessary in the future
        return False
