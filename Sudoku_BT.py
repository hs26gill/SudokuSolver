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
domainList = [1, 2, 3, 4, 5, 6, 7, 8, 9]

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
def select_unassigned_variable(sudoku, row, col):

    ret_cell = list()

    # first check the remaining cols on the current row
    for j in range(col, size):

        # if the current element is unfilled
        if sudoku[row][j] == 0:

            ret_cell = [row, j]

            return ret_cell

    for i in range(row+1, size):

        for j in range(0, size):

            # if the current element is unfilled
            if sudoku[i][j] == 0:

                ret_cell = [i, j]

                return ret_cell

    return ret_cell


# ( Backtrack Algorithm ) returns TRUE if assignment is complete o.w FALSE
def backtrack(sudoku, domain, row, col, unassigned_total, assignments):

    # ( Base case ) return TRUE if the assignment is complete
    if unassigned_total == 0:

        print "Total number of Assignments:", assignments

        return True

    # get the next unassigned/available cell
    var = select_unassigned_variable(sudoku, row, col)
    var_row = var[0]
    var_col = var[1]

    # assign all the available domain values to the cell
    for value in domain[var_row][var_col]:

        unassigned_total -= 1
        sudoku[var_row][var_col] = value

        # check constraints with the assignment of value
        if check_constraints(sudoku, var_row, var_col) is True:

            assignments += 1
            # recurse on the next unassigned variable
            next_row = var_row
            next_col = var_col

            if next_col == ( size - 1 ):

                next_col = 0
                next_row += 1

            else:

                next_col += 1

            # call backtrack on next cell
            result = backtrack(sudoku, domain, next_row, next_col, unassigned_total, assignments)

            # if variable/cell assignment is successful
            if result is True:

                return result

        # remove the variable assignment if constraints are unsatisfied
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
