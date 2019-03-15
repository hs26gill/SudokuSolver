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


# returns the row,col of the next unassigned/available cell in the sudoku
def select_unassigned_variable(domain, row, col):

    emptyDomain = -1

    # check the remaining col
    for j in range(col, size):

        # if the current element is unfilled
        if emptyDomain not in domain[row][j]:

            ret_cell = [row, j]

            return ret_cell

    ret_cell = list()

    for i in range(row+1, size):

        for j in range(0, size):

            # if the current element is unfilled
            if emptyDomain not in domain[i][j]:

                ret_cell = [i, j]

                return ret_cell

    return ret_cell


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


# ( Backtrack Algorithm with Forward checking) returns TRUE if assignment is complete o.w FALSE
def backtrack(sudoku, domain, row, col, unassigned_total, total_assignments):

    # ( Base case ) return TRUE if the assignment is complete
    if unassigned_total == 0:

        print "Total number of Assignments:", total_assignments

        return True

    # get the next unassigned variable
    var = select_unassigned_variable(domain, row, col)
    var_row = var[0]
    var_col = var[1]

    # assign ( potentially all ) the available domain values to the cell
    for value in domain[var_row][var_col]:

        unassigned_total -= 1
        sudoku[var_row][var_col] = value
        total_assignments += 1

        # check constraints with the assignment of value
        if check_constraints(sudoku, var_row, var_col) is True:

            # perform inference ( forward checking ) for any violation due to assignment
            temp_domain = copy_matrix(domain)
            temp_domain[var_row][var_col] = [-1]
            inf_result = inference(temp_domain, var_row, var_col, value)

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
                result = backtrack(sudoku, temp_domain, next_row, next_col, unassigned_total, total_assignments)

                # variable assignment is successful
                if result is True:

                    return result

        # remove the variable assignment if assignment is a violation stop the use of temp_domain
        unassigned_total += 1
        sudoku[var_row][var_col] = 0

    return False


# wrapper for backtrack algorithm
def backtrack_wrapper(sudoku, domain, unassigned_total):

    row = 0
    col = 0
    assignments = 0

    if backtrack(sudoku, domain, row, col, unassigned_total, assignments) is False:

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


