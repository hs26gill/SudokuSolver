# libraries
import sys
import time

# start time
start = time.time()
# input file
filename = str(sys.argv[1])
input_file = open(filename, "r")
# initialize sudoku
size = 9
sudoku = [[0 for i in range(size)] for j in range(size)]
# initialize domain
domain = [[list() for i in range(size)] for j in range(size)]
# unassigned cells counter
unassigned_total = 0
# domain list
domainList = [1, 2, 3, 4, 5, 6, 7, 8, size]

# read input file
for row in range(size):

    # read one line
    cur_row = input_file.readline()
    cur_row = cur_row.split(" ")

    for column in range(size):

        # fill values in sudoku
        sudoku[row][column] = int(cur_row[column])

        # fill cell domain
        if int(cur_row[column]) == 0:

            domain[row][column] = domainList
            unassigned_total += 1

        else:

            # empty/value in domain for already filled cells
            domain[row][column] = [-1]


# CONSTRAINTS CHECK FUNCTIONS

# checks if all cells in row are different
def all_diff_row(sudoku, row):

    filled_values = set()

    for col in range(size):

        # value already used in the row
        if sudoku[row][col] in filled_values:

            return False

        else:

            if sudoku[row][col] != 0:

                filled_values.add(sudoku[row][col])

    return True


# checks if all cells in column are different
def all_diff_col(sudoku, col):

    filled_values = set()

    for row in range(size):

        # value already used in the row
        if sudoku[row][col] in filled_values:

            return False

        else:

            if sudoku[row][col] != 0:

                filled_values.add(sudoku[row][col])

    return True


# helper - checks if cells in given sub-grid are all different
def _sub_grid_unique(sudoku, row, col):

    filled_values = set()

    for i in range(row, row + 3):

        for j in range(col, col + 3):

            if sudoku[i][j] in filled_values:

                return False

            else:

                if sudoku[i][j] != 0:

                    filled_values.add(sudoku[i][j])

    return True


# checks all cells in the 3x3 sub-grid are different
def all_diff_subgrid(sudoku, row, col):

    # check row and col belong to which sub grid
    if (row >= 0) and (row <= 2):

        if (col >= 0) and (col <= 2):

            return _sub_grid_unique(sudoku, 0, 0)

        elif (col >= 3) and (col <= 5):

            return _sub_grid_unique(sudoku, 0, 3)

        else:

            return _sub_grid_unique(sudoku, 0, 6)

    elif (row >= 3) and (row <= 5):

        if (col >= 0) and (col <= 2):

            return _sub_grid_unique(sudoku, 3, 0)

        elif (col >= 3) and (col <= 5):

            return _sub_grid_unique(sudoku, 3, 3)

        else:

            return _sub_grid_unique(sudoku, 3, 6)
    else:

        if (col >= 0) and (col <= 2):

            return _sub_grid_unique(sudoku, 6, 0)

        elif (col >= 3) and (col <= 5):

            return _sub_grid_unique(sudoku, 6, 3)

        else:

            return _sub_grid_unique(sudoku, 6, 6)


# check if all constraints ( row, col, sub-grid are different ) are satisfied after the new cell assignment
def check_constraints(sudoku, row, col):

    # row
    row_cells_unique = all_diff_row(sudoku, row)
    # column
    col_cells_unique = all_diff_col(sudoku, col)
    # sub-grid
    subgrid_cells_unique = all_diff_subgrid(sudoku, row, col)

    if not row_cells_unique or not col_cells_unique or not subgrid_cells_unique:

        return False

    else:

        return True


# returns true if cell is present in visited_cells o.w false
def in_list(visited_cells, cell):
    for i in range(len(visited_cells)):
        if cell == visited_cells[i]:
            return True
    return False


# returns number of unassigned cells in the given subgrid ( row, col are top-left corner of subgrid )
def unassigned_subgrid_cells(domain, row, col, visited_list):
    total = 0
    for i in range(row, row + 3):
        for j in range(col, col + 3):
            mylist = [i,j]
            if not in_list(visited_list, mylist):
                total += 1
    return total


# return the number of unassigned neighbours of given cell ( cell_row, cell_col )
def unassigned_neighbour(domain, cell_row, cell_col):

    assigned_cell = -1
    total = 0
    checked_list = list(list())

    # row
    for i in range(size):

        if assigned_cell not in domain[cell_row][i]:

            total += 1
            checked_list.append([cell_row, i])

    # column
    for i in range(size):

        if assigned_cell not in domain[i][cell_col]:

            total += 1
            checked_list.append([i, cell_col])

    # sub-grid
    if (cell_row >= 0) and (cell_row <= 2):

        if (cell_col >= 0) and (cell_col <= 2):

            return total + unassigned_subgrid_cells(domain, 0, 0, checked_list)

        elif (cell_col >= 3) and (cell_col <= 5):

            return total + unassigned_subgrid_cells(domain, 0, 3, checked_list)

        else:

            return total + unassigned_subgrid_cells(domain, 0, 6, checked_list)

    elif (cell_row >= 3) and (cell_row <= 5):

        if (cell_col >= 0) and (cell_col <= 2):

            return total + unassigned_subgrid_cells(domain, 3, 0, checked_list)

        elif (cell_col >= 3) and (cell_col <= 5):

            return total + unassigned_subgrid_cells(domain, 3, 3, checked_list)

        else:

            return total + unassigned_subgrid_cells(domain, 3, 6, checked_list)

    else:
        if (cell_col >= 0) and (cell_col <= 2):

            return total + unassigned_subgrid_cells(domain, 6, 0, checked_list)

        elif (cell_col >= 3) and (cell_col <= 5):

            return total + unassigned_subgrid_cells(domain, 6, 3, checked_list)

        else:

            return total + unassigned_subgrid_cells(domain, 6, 6, checked_list)


# returns the next best available/unassigned cell ( row, col ) using the following heuristics.
# minimum-remaining-values (MRV): Choose the cell with the fewest values left in its domain.
# degree heuristic: Choose the cell that is involved in the largest number of
# constraints on other unassigned cells
def select_unassigned_variable(domain):

    # domain value for assigned cell
    assigned_cell = -1
    # current best Minimum Remaining Values (mrv) in the domain of a cell
    mrv_value = 10
    # hold the cells with minimum remaining values in the domain
    mrv_list = list(list())

    for i in range(size):

        for j in range(size):

            # if mrv of domain encountered at ( i, j ) cell < mrv_value, clear the list and update the value
            if assigned_cell not in domain[i][j]:

                if len(domain[i][j]) == mrv_value:

                    mrv_list.append([i, j])

                if len(domain[i][j]) < mrv_value:

                    mrv_list = list(list())
                    mrv_list.append([i, j])
                    mrv_value = len((domain[i][j]))

    # no need for degree heuristics if only one item mrv
    if len(mrv_list) == 1:

        return mrv_list

    # degree heuristics for multiple cells with same mrv
    else:

        # contains the cell with largest available/unassigned neighbours
        hrv_list = list(list())
        # assign with total unassigned neighbours for the first cell in mrv list
        hrv_list.append(mrv_list[0])
        hrv_value = unassigned_neighbour(domain, mrv_list[0][0], mrv_list[0][1])

        for i in range(len(mrv_list)):

            total_neighbour = unassigned_neighbour(domain, mrv_list[i][0], mrv_list[i][1])

            if total_neighbour > hrv_value:

                hrv_list = list(list())
                hrv_list.append(mrv_list[i])
                hrv_value = total_neighbour

        return hrv_list


# returns a copy of all the domains of the sudoku
def copy_matrix(domain):

    matrix = [[list() for i in range(size)] for j in range(size)]

    for i in range(size):

        for j in range(size):

            matrix[i][j] = list(domain[i][j])

    return matrix


# remove value from domain and check for any violations in the given sub-grid
def sub_grid_reduce_domain(domain, row, col, value):

    for i in range(row, row + 3):

        for j in range(col, col + 3):

            if value in domain[i][j]:

                domain[i][j].remove(value)

                # if the domain becomes empty we cannot use the value
                if len(domain[i][j]) == 0:

                    return False
    return True


# assigns value and performs forward Checking on the sudoku
def inference(domain, row, col, value):

    # reduce the domain of the row cells
    for i in range(size):

        if value in domain[row][i]:

            domain[row][i].remove(value)

            if len(domain[row][i]) == 0:

                return False

    # reduce the domain of the col cells
    for i in range(size):

        if value in domain[i][col]:

            domain[i][col].remove(value)

            if len(domain[i][col]) == 0:

                return False

    # reduce the domain of the sub-grid
    # check which sub-grid the cell is present in.
    if (row >= 0) and (row <= 2):

        if (col >= 0) and (col <= 2):

            return sub_grid_reduce_domain(domain, 0, 0, value)

        elif (col >= 3) and (col <= 5):

            return sub_grid_reduce_domain(domain, 0, 3, value)

        else:

            return sub_grid_reduce_domain(domain, 0, 6, value)

    elif (row >= 3) and (row <= 5):

        if (col >= 0) and (col <= 2):

            return sub_grid_reduce_domain(domain, 3, 0, value)

        elif (col >= 3) and (col <= 5):

            return sub_grid_reduce_domain(domain, 3, 3, value)

        else:

            return sub_grid_reduce_domain(domain, 3, 6, value)

    else:
        if (col >= 0) and (col <= 2):

            return sub_grid_reduce_domain(domain, 6, 0, value)

        elif (col >= 3) and (col <= 5):

            return sub_grid_reduce_domain(domain, 6, 3, value)

        else:

            return sub_grid_reduce_domain(domain, 6, 6, value)


# return the best value available to use for assignment using least constraining value heuristics
# on the subgrid
def subgrid_lcv(sudoku, domain, row, col, visited_list, dict):

    assigned_cell = -1

    for i in range(row, row + 3):

        for j in range(col, col + 3):

            cell = [i,j]

            if not in_list(visited_list, cell):

                for key in domain[i][j]:

                    if key == assigned_cell:

                        key = sudoku[i][j]

                    # dictionary of values and number of time they are used
                    if key in dict:

                        dict[key] = dict[key] + 1

    minval = min(dict.values())

    for key in dict.keys():

        if dict[key] == minval:

            return key


# returns best value for the current unassigned cell ( row, col ) using the following heuristic.
# least-constraining-value (LCV): get the value that leaves the maximum number of values for the
# neighbouring unassigned cells
def least_constraint_value(sudoku, domain, row, col):

    # visited cells;
    visited = list(list())
    visited.append([row, col])
    # available domain value for the current cell
    vals_available = list(domain[row][col])
    # assigned_cell
    assigned_cell = -1
    # dictionary to keep track of the domain values and occurrences in the domain of the neighbours
    dict = {}

    for value in vals_available:
          dict[value] = 0

    # increment the occurrence of values for the cell row
    for i in range(size):

        cur_cell = [row, i]

        # only go to the unassigned cell
        if not in_list(visited, cur_cell):

            for key in domain[row][i]:

                if key in dict:

                    dict[key] = dict[key] + 1
                    # add the current cell to the visited list
                    visited.append([row, i])

    # increment the occurrence of values for the cell column
    for i in range(size):

        cur_cell = [i, col]

        if not in_list(visited, cur_cell):

            for key in domain[i][col]:

                if key in dict:

                    dict[key] = dict[key] + 1
                    visited.append([i, col])

    # increment the occurrence of values for the cell sub-grid
    if (row >= 0) and (row <= 2):

        if (col >= 0) and (col <= 2):

            return subgrid_lcv(sudoku, domain, 0, 0, visited, dict)

        elif (col >= 3) and (col <= 5):

            return subgrid_lcv(sudoku, domain, 0, 3, visited, dict)

        else:

            return subgrid_lcv(sudoku, domain, 0, 6, visited, dict)

    elif (row >= 3) and (row <= 5):

        if (col >= 0) and (col <= 2):

            return subgrid_lcv(sudoku, domain, 3, 0, visited, dict)

        elif (col >= 3) and (col <= 5):

            return subgrid_lcv(sudoku, domain, 3, 3, visited, dict)

        else:

            return subgrid_lcv(sudoku, domain, 3, 6, visited, dict)
    else:

        if (col >= 0) and (col <= 2):

            return subgrid_lcv(sudoku, domain, 6, 0, visited, dict)

        elif (col >= 3) and (col <= 5):

            return subgrid_lcv(sudoku, domain, 6, 3, visited, dict)

        else:

            return subgrid_lcv(sudoku, domain, 6, 6, visited, dict)


# ( Backtrack Algorithm with Forward checking and Heuristic search ( LCV, MRV, degree ))
# returns TRUE if assignment is complete o.w FALSE
def backtrack(sudoku, domain, unassigned_total, total_assignments):

    # ( Base case ) return TRUE if the assignment is complete
    if unassigned_total == 0:

        print "Total number of Assignments:", total_assignments
        return True

    # best available cell/variable using MRV and degree heuristics
    var = select_unassigned_variable(domain)
    var_row = var[0][0]
    var_col = var[0][1]

    # assignment of all the domain values of the var
    for value in range(len(domain[var_row][var_col])):

        # best value for using LCV heuristic
        least_value = least_constraint_value(sudoku, domain, var_row, var_col)
        # assignment
        unassigned_total -= 1
        sudoku[var_row][var_col] = least_value
        total_assignments += 1

        # check constraints with the assignment of value
        if check_constraints(sudoku, var_row, var_col) is True:

            # perform inference ( forward checking ) for any violation due to assignment
            temp_domain = copy_matrix(domain)
            temp_domain[var_row][var_col] = [-1]
            inf_result = inference(temp_domain, var_row, var_col, least_value)

            # if the assignment is good then just use the temp_domain for backtracking
            if inf_result is True:

                # recurse on the next unassigned variable
                next_row = var_row
                next_col = var_col

                if var_col == ( size - 1 ):

                    next_col = 0
                    next_row += 1

                else:

                    next_col += 1

                # call backtrack on next available cell
                result = backtrack(sudoku, temp_domain, unassigned_total, total_assignments)

                # variable assignment is successful
                if result is True:

                    return result

        # remove the variable assignment if assignment is a violation stop the use of temp_domain
        # remove value from the domain, can't use it anymore
        domain[var_row][var_col].remove(least_value)
        unassigned_total += 1
        sudoku[var_row][var_col] = 0

    return False


# wrapper for backtrack algorithm
def backtrack_wrapper(sudoku, domain, unassigned_total):

    assignments = 0

    if backtrack(sudoku, domain, unassigned_total, assignments) is False:

        print ( " FAILURE: Could not solve sudoku " )

    else:

        print ( "************************** SUDOKU COMPLETED ********************************" )
        # print completed Sudoku
        for i in range(size):

            print(sudoku[i])

        print ( "****************************************************************************" )


# call backtrack
backtrack_wrapper(sudoku, domain, unassigned_total)

# finishing time of sudoku
end = time.time()

# execution time of sudoku
print "Total execution time of sudoku:", end - start
