# Sudoku Puzzle
Sudoku is an easy to learn number placement puzzle. It consists of 
81 cells which are divided into nine columns, rows and sub-grid regions. 
The purpose of the player is to place the numbers from 1 to 9 into the 
empty cells in such a way that in every row, column and 3×3 region each number appears only once.

# Sudoku solver
There are three different versions of Sudoku Solvers:

  - __Sudoku_BT.py__ - solves sudoku puzzle using recursive backtracking algorithm 
  - __Sudoku_FC.py__ - solves sudoku puzzle using backtracking and forward checking
  - __Sudoku_Heuristics.py__ - Uses Heuristic ( minimum-remaining-values, least-constraining-value,
   degree heuristic) in addition to backtracking and forward checking to solve a given sudoku

# How To Run
An input file is required to run each of the sudoku solver. For example:


__input_file.txt__

```

0 1 9 2 5 4 0 7 6
2 4 3 6 7 1 8 5 9
5 7 6 8 9 3 2 4 1
3 5 0 9 6 7 1 8 0
1 8 7 3 4 5 0 9 2
9 6 4 1 0 2 0 3 5
7 2 1 4 0 9 5 6 8
4 3 8 5 2 6 9 0 7
6 9 5 7 1 8 4 0 3

```

__NOTE:__ "0" represents the cells which are not filled.


Use the example command below to run the program:

```
$ python Sudoky_BT.py Input_file.txt 
``` 


# Output
The program outputs the following information when run:

    - Totol number of cells it filled
    - Prints the complete sudoku if the program finishes
    - Total completion time
    
For example:

```

Total number of Assignments: 10
************************** SUDOKU COMPLETED ********************************
[8, 1, 9, 2, 5, 4, 3, 7, 6]
[2, 4, 3, 6, 7, 1, 8, 5, 9]
[5, 7, 6, 8, 9, 3, 2, 4, 1]
[3, 5, 2, 9, 6, 7, 1, 8, 4]
[1, 8, 7, 3, 4, 5, 6, 9, 2]
[9, 6, 4, 1, 8, 2, 7, 3, 5]
[7, 2, 1, 4, 3, 9, 5, 6, 8]
[4, 3, 8, 5, 2, 6, 9, 1, 7]
[6, 9, 5, 7, 1, 8, 4, 2, 3]
****************************************************************************
Total execution time of sudoku: 0.00337696075439


```

# Programming Language Used

Python
