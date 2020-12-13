

import math
from pygame.sprite import collide_circle
import csp
import numpy as np
from copy import deepcopy

class Util:

    def __init__(self, human=False):

        self.human = human
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
    
    def refactorDomains(self,val, var, domains):
        '''
        After every assignment, refactor the domains of all effected cells.
        '''
        x,y = var

        box_num = 0
        boxx, boxy = (math.floor(x/3), math.floor(y/3))
        if boxx == 0:
            box_num = boxy
        if boxx == 1:
            box_num = boxy + 3
        if boxx == 2:
            box_num = boxy + 6    

        for cell in self.box_dictionary[box_num]:
            try:
                if not var == cell:
                    domain = domains[cell]
                    domain.remove(val)
                    domains[cell] = domain
            except ValueError:
                pass

        for i in range(9):
            try:
                if not var == (x,i):
                    domain = domains[(x,i)]
                    domain.remove(val)
                    domains[(x,i)] = domain
            except ValueError:
                pass

            try:
                if not var == (i,y):
                    domain = domains[(i,y)]
                    domain.remove(val)
                    domains[(i,y)] = domain
            except ValueError:
                pass

        if self.human:
            comparison = None
            while not comparison == domains:

                comparison = deepcopy(domains)

                domains = self.naked_set(domains)
                domains = self.pointing_set(domains)
                domains = self.box_reduction(domains)


            
    def hasSingleton(self, domain, cell_list):
        '''
        Checks if a cell_list has at least one cell with a singleton domain
        
        Returns: A Boolean
        '''
        for cell in cell_list:
            if len(domain[cell]) == 1:
                return True
        return False

    def allDiff(self, csp, cell_list):
        '''
        Implementation of pseduocode 6.2.5 Global Constraints: AI, A Modern Approach 4e. (pg 188-189)
        Checks to see if any assigned variables have conflictions (are the same assignment)

        Returns: A boolean
        '''
        domains = csp.domains
        cell_list = cell_list.copy()

        domain_tracker = [*range(1,10)] 

        # while there are singleton domain variables left in cell_list
        while self.hasSingleton(domains, cell_list):

            # for all cells in the constraint
            for cell in cell_list:
                domain = domains[cell]  

                # remove a cell that has singleton domain
                if len(domain) == 1:
                    cell_list.remove(cell)
                    val = domain[0] 
                    if val in domain_tracker:
                        domain_tracker.remove(val)
                    else:
                        return False

                    # delete the cell's value from the domain of remaining  
                    for remaining in cell_list:
                        d = set(domains[remaining])
                        d.discard(val)
                        domains[remaining] = list(d)

        return True

    def abstractRow(self,index):
        row = []
        for i in range(0,9):
            row.append((index,i))
        return row
    
    def abstractCol(self,index):
        col = []
        for i in range(0,9):
            col.append((i, index))
        return col 
    
    def abstractBox(self, index):
        return self.box_dictionary[index]

    def remove_if_in_domain(self, values, domains, cells):

        # this function removes values from the domain 
        # of cells wherever it occurs

        for val in values:
            for cell in cells:
                if val in domains[cell]:
                    domains[cell].remove(val)

        return domains

    def find_box(self, cell):

        # this function returns the int corresponding to the box
        # that the cell is located in 

        for box in self.box_dictionary:

            if (cell in self.box_dictionary[box]):
                return box

        return None


    def naked_set(self, domains):   

        # this function should recognize when a unique set of values 
        # share the same unique cells. This is only applied when the 
        # cells are in the same box, column, or row. The domain is then
        # pruned to remove those values from remaining cells in the same
        # box, column, or row.

        comparison = None

        # while loop is so that we check for naked sets multiple times until we ensure 
        # no more exist. By pruning values, we might be creating new naked sets, so we 
        # have to check again.
        while(not domains == comparison):

            # Must create a deep copy because python is passing by reference. We are
            # changing the internal domains contained in the dictionary. Deep copy will
            # copy those internal domains instead of just a copy of the dictionary with 
            # pointers to the same domains
            comparison = deepcopy(domains)

            for row in np.arange(9):
                cells = []

                for col in np.arange(0,9):
                    # add every cell in this column
                    cells.append((row, col))
                    
                # look for naked sets in each column
                domains = self.naked_set_helper(domains, cells)

            for col in np.arange(0,9):
                cells = []

                for row in np.arange(0,9):
                    # add every cell in this row
                    cells.append((row, col))
                
                # look for naked sets in each row
                domains = self.naked_set_helper(domains, cells)

            for box in self.box_dictionary:
                domains = self.naked_set_helper(domains, self.box_dictionary[box])
            
        return domains


    def naked_set_helper(self, domains, cells):

        # keep track of the unique domains and all domains we come across
        # (all_domains will be used to refer to frequency of a domain)
        unique_domains = []
        all_domains = []

        # for each set in this row/col/box
        for cell in cells:

            # if domain of this cell is not in unique_domains, place it in there
            if not domains[cell] in unique_domains:
                unique_domains.append(domains[cell])

            # add domain to all_domains 
            all_domains.append(domains[cell])

        # looking at each unique domain
        for domain in unique_domains:

            # check if it occurs more than once
            # check that the frequency is equal to number of values in that domain
            # if both these conditions are satisfied, we found a naked set 
            if all_domains.count(domain) > 1 and all_domains.count(domain) == len(domain):

                # now we are going to check the domains of all the other cells
                for cell in cells:

                    # if this domain is the naked set we found, ignore it
                    if set(domains[cell]) == set(domain):
                        continue
                    
                    domains = self.remove_if_in_domain(domain, domains, [cell])
                            
        return domains

    def pointing_set(self, domains):

        comparison = None

        while(not domains == comparison):

            comparison = deepcopy(domains)

            # for this technique, we want to check if the values in a box
            # only occur in the same row or column. If that were the case,
            # we can remove that value in the remainder of the row/column
            for box in self.box_dictionary:
                new_domains = self.pointing_set_helper(domains, box)

        return domains



    def pointing_set_helper(self, domains, box):

        # iterate through each possible number 

        for n in np.arange(1,10):

            # hold all the rows and cols containing n
            rows = []
            cols = []

            for cell in self.box_dictionary[box]:

                if n in domains[cell]:
                    rows.append(cell[0])
                    cols.append(cell[1])

            rows = list(set(rows))
            cols = list(set(cols))

            # checking that a number is contained in only one row but multiple columns will
            # stop us from executing the case where we have a singleton domain
            if len(rows) == 1 and len(cols) > 1:
                
                row = rows[0]
                cells = []

                # identify all the cells in that row but not in that box
                for col in np.arange(0,9):
                    if not (row, col) in self.box_dictionary[box]:
                        cells.append((row, col))

                domains = self.remove_if_in_domain([n], domains, cells)

            elif len(cols) == 1 and len(rows) > 1:
                col = cols[0]
                cells = []

                for row in np.arange(0,9):
                    if not (row, col) in self.box_dictionary[box]:
                        cells.append((row, col))

                domains = self.remove_if_in_domain([n], domains, cells)

        return domains

    def box_reduction(self, domains):

        comparison = None

        while(not domains == comparison):

            comparison = deepcopy(domains)

            # for this technique, we want to check if the values in a row or column
            # only occur in the same box. If that were the case,
            # we can remove that value in the remainder of the box
            for row in np.arange(9):
                cells = []

                for col in np.arange(9):
                    # add every cell in this column
                    cells.append((row, col))
                    
      
                # look for box reduction in each column
                domains = self.box_redux_helper(domains, cells)


            for col in np.arange(9):
                cells = []

                for row in np.arange(9):
                    # add every cell in this row
                    cells.append((row, col))
                
                # look for naked sets in each row
                domains = self.box_redux_helper(domains, cells)

        return domains

    def box_redux_helper(self, domains, cells):

        # iterate through each possible number 

        for n in np.arange(1,10):

            # hold the boxes containing n
            boxes = []

            for cell in cells:

                if n in domains[cell] :
                    box = self.find_box(cell)
                    boxes.append(box)

            boxes = list(set(boxes))

            

            # checking that a number is contained in only one box
            if len(boxes) == 1:
                
                box = boxes[0]

                # identify all the cells in that box but not in that row/col 
                remove_cells = []
                
                for cell in self.box_dictionary[box]:
                    if not cell in cells:
                        remove_cells.append(cell)

                domains = self.remove_if_in_domain([n], domains, remove_cells)

        return domains

