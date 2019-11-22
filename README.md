# 590PZ-Project
Forks of this are student projects for IS 590PZ
Game: Fillomino Puzzle Generator and Solver

# Description
Fillomino game was published in 1994 by Nikoli (Japanese Magazine). It is played on a rectangular grid with random grid size, where some of the cells contain numbers called as "givens". The goal of the player in this game is to divide the grid into blocks called as polyminoes such that each given number x is a part of the grid of n-omino. No two same-sized blocks can touch each other either horizontally or vertically.

# Libraries used
- numpy
- click
- math
- random
- scipy.ndimage.label
- copy

# Implementation:
- Our program generates a grid of varied size and levels based on user's choice
      - Grid Size: 10 x 5, 10 x 10
      - Game Level: Easy, Medium, Hard
- The program initially generates a valid board using Breadth First Search where it iterates over each cell and fills it to form variety of continuous regions. Choosing of neighbors for a given cell is done randomly.
- Each time a board is generated, it is checked for validity and the process continues till a valid board is generated.
- Once a valid board is generated, some cells would be filled initially with numbers/clues that are immutable and other numbers will be masked with a 0.
- The final masked board is then displayed to the player and is asked for input with format (row, column, value).


