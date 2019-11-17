"""
Fillomino Puzzle solver and Generator

Authors: Gaurav Dharra, Harshitha Ravindra
"""

import numpy as np
import click
from scipy.ndimage import label, generate_binary_structure
import math, random


def generate_board(num_rows, num_columns):
    """
    Method that generates a 2d numpy array with all zero values for
    given number of row and column values.
    :param num_rows: integer indicating number of rows
    :param num_columns: integer indicating number of rows
    :param list_digits:
    :return: Returns a 2d array of the required size with all zeros
    """
    grid = np.zeros((num_rows, num_columns), int)
    list_digits = generate_possible_numbers(num_rows, num_columns)
    random.shuffle(list_digits)
    list_digits = [j for i in list_digits for j in i]

    counter = 0

    for x in range(num_rows):
        for y in range(num_columns):
            print(counter)
            if grid[x, y] == 0:
                if counter < len(list_digits):
                    grid[x, y] = list_digits[counter]
                    j = grid[x, y]
                    counter += 1
                    coord = [x, y]
                    while j > 1:
                        neighbor = get_neighbors(coord)
                        neighbor = [[m, n] for (m, n) in neighbor
                                    if 0 <= m < num_rows and 0 <= n < num_columns
                                    and grid[m, n] == 0]
                        # TODO: Think of a logic for back tracing if no neighbors are found
                        if len(neighbor) > 0:
                            neighbor = random.choice(neighbor)
                            if counter < len(list_digits):
                                grid[neighbor[0], neighbor[1]] = list_digits[counter]
                            else:
                                break
                            counter += 1
                            coord = [neighbor[0], neighbor[1]]
                            j -= 1
                        elif len(neighbor) == 0:
                            break
                        print(grid)
                else:
                    # TODO: Logic to append 1s in the grid
                    grid[x, y] = 1
                    counter += 1
            print(grid)


def game_level():
    """

    :return:
    """
    game_option = click.prompt('Please select difficulty level: \n \
        Enter 1 for easy (10 X 5) \n  \
        Enter 2 for medium (10 X 10) \n \
        Enter 3 for difficult (20 X 20)', type=click.IntRange(1, 3))
    if game_option == 1:
        m = 10
        n = 5
    elif game_option == 2:
        m = 10
        n = 10
    else:
        m = 20
        n = 20
    return m, n


def is_correct_solution(current_board, solution):
    """
    Method returns a boolean value indicating if the solution is correct based on the following:
    - Validates if the board is filled
    - If board is filled, compares it to the solution
    :param current_board: 2d numpy array indicating the board filled based on the player input
    :param solution: 2d numpy array indicating the predefined solution
    :return: boolean indicating the correctness of the solution
    """
    if not np.count_nonzero(current_board) == np.size(current_board):
        print('Board is not filled')
        return False
    else:
        if np.array_equal(current_board, solution):
            print('Correct solution')
            return True
        else:
            print('Incorrect solution')
            return False


def input_coordinates():
    """
    Asks for user inputs to populate the board
    :return: User entered coordinate and value of the board
    """
    coord = click.prompt('Enter the the cell to be filled in the format\n  row, col, value')
    val = coord.split(',')
    input_coord = [int(x) for x in val if int(x)]
    if len(input_coord) != 3:
        input_coordinates()
    return input_coord


def check_continuity(current_board, input_coord):
    """

    :param current_board:
    :param input_coord:
    :return:
    """
    continuous = False
    val = input_coord[2]
    neighbors = get_neighbors(input_coord)
    board_shape = current_board.shape
    for [x, y] in neighbors:
        if x < 0 or y < 0 or x >= board_shape[0] or y >= board_shape[1]:
            continue
        else:
            cell_value = current_board[x, y]
            if cell_value == 0 or cell_value == val:
                continuous = True
                break
    return continuous


def get_neighbors(input_coord):
    row = input_coord[0]
    col = input_coord[1]
    return [[row-1, col], [row+1, col], [row, col-1], [row, col+1]]


def check_number_of_cells(current_board, input_coord, counter, has_zero_flag, previous_coord):
    """
    Performing BFS to compute number of cells.
    :param current_board:
    :param input_coord:
    :param counter:
    :param has_zero_flag:
    :param previous_coord:
    :return:
    """
    val = input_coord[2]
    neighbors = get_neighbors(input_coord)
    board_shape = current_board.shape

    new_coord = []
    for [x, y] in neighbors:
        if x < 0 or y < 0 or x >= board_shape[0] or y >= board_shape[1] or [x, y] == previous_coord:
            continue
        else:
            cell_value = current_board[x, y]
            if cell_value == val:
                counter += 1
                new_coord.append([x,y])
            elif cell_value == 0:
                has_zero_flag = True

    if len(new_coord) == 0:
        if counter == val:
            return True
        elif has_zero_flag and counter<val:
            return True
        else:
            return False
    else:
        for [x, y] in new_coord:
            return check_number_of_cells(current_board, [x, y, current_board[x,y]], counter, has_zero_flag, [input_coord[0], input_coord[1]])


def generate_possible_numbers(grid_row, grid_col):
    """
    Generates a 2d list of numbers in a deterministic way based on the formula (1 / total_digits) * (grid_size / digit)
    in an iterative manner. The iteration continues for a threshold of 95% of grid size.
    Remaining values are filled by 1.
    Additionally, counter can be updated later to increase complexity
    :param grid_row:
    :param grid_col:
    :return: 2d list
    """
    if grid_col == 5:
        total_digits = 5
    elif grid_row == 20:
        total_digits = 9
    else:
        total_digits = 7
    grid_size = grid_row * grid_col
    region_size = 0
    num_list = []
    # counter = 1
    while region_size <= 0.95*grid_size:
        for i in range(2, total_digits+1):
            # for j in range(math.floor(counter*(grid_size-region_size)/(total_digits-1)/i)):
            for j in range(math.floor((grid_size - region_size) / (total_digits - 1) / i)):
                num_list.append([i]*i)
        a = sum([len(x) for x in num_list])
        if a == region_size:
            break
        else:
            region_size = a
            # counter += 1
        print(region_size)

    # num_list.extend([[1]] * (grid_size-region_size))

    return num_list


def get_masked_array(board):
    """

    :param board:
    :return: labeled array
    """
    elements = np.unique(board)
    to_mask_board = np.zeros(board.shape)
    labeled_array = []
    num_features = []
    for i in elements:
        truth_board = (board == i)
        truth_board_val = board * truth_board
        each_labeled_array, each_num_features = label(truth_board_val)
        labeled_array.append(each_labeled_array)
        num_features.append(each_num_features)
    return labeled_array, num_features


def mask_board(board):
    """

    :param board:
    :return:
    """
    labeled_array, num_features = get_masked_array(board)
    to_mask_board = np.zeros(board.shape)
    for i in range(len(num_features)):
        for j in range(1, num_features[i] + 1):
            masked_matrix = (labeled_array[i] == j)
            indices = np.where(masked_matrix)
            to_keep = np.random.choice(range(len(indices[1])))
            to_mask_board[indices[0][to_keep], indices[1][to_keep]] = 1
    masked_board = board * to_mask_board
    return masked_board


