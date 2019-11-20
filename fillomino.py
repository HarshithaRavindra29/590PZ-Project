"""
Fillomino Puzzle solver and Generator

Authors: Gaurav Dharra, Harshitha Ravindra
"""

import numpy as np
import click
from scipy.ndimage import label, generate_binary_structure
import math
import random
import copy


def get_masked_array(board):
    """
    This function generates a board that has the shape of each of the elements using scipy.
    it is used in couple of functions below,
    1. using the shape of the elements to hide other elements and keep 1
    2. To generate board
    :param board:
    :return: labeled array and number of regions
    """
    elements = np.unique(board)
    labeled_array = []
    num_features = []
    for i in elements:
        truth_board = (board == i)
        truth_board_val = board * truth_board
        each_labeled_array, each_num_features = label(truth_board_val)
        labeled_array.append(each_labeled_array)
        num_features.append(each_num_features)
    return labeled_array, num_features


def check_board_valid(grid, list_digits):
    """

    :param grid:
    :param list_digits:
    :return:
    """
    labeled_array, num_features = get_masked_array(grid)
    elements = np.unique(grid)
    is_grid_valid = True
    for idx, i in enumerate(elements):
        if list_digits.count(i) / i != num_features[idx]:
            is_grid_valid = is_grid_valid and False
        else:
            for j in range(1, num_features[idx] + 1):
                counter_board = labeled_array[idx] == j
                if np.count_nonzero(counter_board) != i:
                    is_grid_valid = is_grid_valid and False

    return is_grid_valid


def generate_board(num_rows, num_columns):
    """
    Method that generates a 2d numpy array of game for
    given number of row and column values.
    :param num_rows: integer indicating number of rows
    :param num_columns: integer indicating number of rows
    :return: Returns a 2d array of the required size Game board
    """
    print("Waiting for board to be generated .............")
    list_digits_2d = generate_possible_numbers(num_rows, num_columns)
    is_grid_valid = False
    iteration = 0
    while not is_grid_valid:
        # shuffle the 2d list of all possible combinations
        random.shuffle(list_digits_2d)
        # convert the 2d list into a 1d list
        list_digits = [j for i in list_digits_2d for j in i]
        grid = np.zeros((num_rows, num_columns), int)
        # counter to keep a track of number of grid positions filled
        counter = 0
        # grid position not filled is a 2d array to keep track of all positions not filled
        grid_positions_not_filled = [[x, y] for x in range(num_rows) for y in range(num_columns)]
        # print('I am here ', (iteration + 1))
        while len(grid_positions_not_filled) > 0:
            # Take the 1st empty element of the grid
            x = grid_positions_not_filled[0][0]
            y = grid_positions_not_filled[0][1]
            if grid[x, y] == 0:
                if counter < len(list_digits):
                    grid[x, y] = list_digits[counter]
                    total_iterations = j = grid[x, y]
                    counter += 1
                    coord = [x, y]
                    grid_positions_not_filled.remove(coord)
                    previous_coord = {}
                    while j > 1:
                        neighbor = get_neighbors(coord)
                        neighbor = [[m, n] for (m, n) in neighbor
                                    if 0 <= m < num_rows and 0 <= n < num_columns
                                    and grid[m, n] == 0
                                    and grid[m, n] != total_iterations]
                        previous_coord[(coord[0], coord[1])] = neighbor
                        if len(neighbor) > 0:
                            neighbor = random.choice(neighbor)
                            if counter < len(list_digits):
                                grid[neighbor[0], neighbor[1]] = list_digits[counter]
                                grid_positions_not_filled.remove(neighbor)
                                counter += 1
                                coord = [neighbor[0], neighbor[1]]
                                j -= 1
                            else:
                                j = 1
                        elif len(neighbor) == 0:
                            previous_coord.popitem()
                            if len(previous_coord) > 0:
                                neighbors_prev = previous_coord.get(list(previous_coord.keys())[-1])
                                neighbors_prev.remove(coord)
                                if len(neighbors_prev) > 0:
                                    coord = random.choice(neighbors_prev)
                                    grid[coord[0], coord[1]] = list_digits[counter]
                                    grid_positions_not_filled.remove(coord)
                                    counter += 1
                                    j -= 1
                                else:
                                    if grid[coord[0], coord[1]] != 0:
                                        grid[coord[0], coord[1]] = 0
                                        counter -= 1
                                        grid_positions_not_filled.append([coord[0], coord[1]])
                                    j = 1
                            else:
                                grid[coord[0], coord[1]] = 1
                                try:
                                    ind = list_digits.index(1, counter-1, len(list_digits)-1)
                                    del list_digits[ind]
                                    list_digits.insert(counter-1, 1)
                                except ValueError:
                                    j = 1
                                j = 1
                else:
                    grid[x, y] = 1
                    grid_positions_not_filled.remove([x, y])
                    counter += 1
        is_grid_valid = True
        is_grid_valid = is_grid_valid and check_board_valid(grid, list_digits)
        if not is_grid_valid:
            iteration += 1
    return grid, list_digits, iteration


def game_level():
    """
    Takes user input on the game level and returns the size of the corresponding board
    :return: row and column size of the board
    """
    game_option = click.prompt('Please select difficulty level: \n \
        Enter 1 for easy (10 X 5) \n  \
        Enter 2 for medium (10 X 10) \n \
        Enter 3 for difficult (10 X 15)', type=click.IntRange(1, 3))
    if game_option == 1:
        m = 10
        n = 5
    elif game_option == 2:
        m = 10
        n = 10
    else:
        m = 10
        n = 15
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
    # TODO validation on only int input within range of m and n needs to be implemented
    input_coord = [int(x) for x in val]
    if len(input_coord) != 3:
        print("Wrong input, try again")
        input_coordinates()
    return input_coord


def check_continuity(current_board, input_coord):
    """
    As the player inputs the the coordinates to populate the board, this function checks if
    the player is giving values for a continous region, if not it would
    promt the player
    :param current_board:
    :param input_coord:
    :return: Boolean
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
    """
    This function is used to get the neighbours of the cell of interest in the board
    :param input_coord:
    :return: Values of the neighbouring cells
    """
    row = input_coord[0]
    col = input_coord[1]
    return [[row-1, col], [row+1, col], [row, col-1], [row, col+1]]


def check_number_of_cells(current_board, input_coord):
    """
    Performing BFS to compute number of cells.
    :param current_board:
    :param input_coord:
    :return:
    """
    val = input_coord[2]
    cloned_board = copy.deepcopy(current_board)
    cloned_board[input_coord[0], input_coord[1]] = val
    labeled_board, num_feat = get_masked_array(cloned_board)
    label_to_be_verified = labeled_board[val]
    feature_number = label_to_be_verified[input_coord[0], input_coord[1]]
    feature_length = np.count_nonzero(label_to_be_verified == feature_number)
    if feature_length > val:
        return False
    return True



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
        total_digits = 6
    elif grid_row == 15:
        total_digits = 9
    else:
        total_digits = 9
    grid_size = grid_row * grid_col
    region_size = 0
    num_list = []
    # counter = 1
    while region_size <= 0.90*grid_size:
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

    num_list.extend([[1]] * (grid_size-region_size))

    return num_list


def mask_board(board):
    """
    This function takes the generated board and hides elements and creates a puzzle for the
    player to solve.
    For every type of number, only 1 element is displayed. for example if the board is [[1,2,2],[2,3,3],[2,1,3]]
    [[1,2,0],[0,3,0],[2,1,0]] is created.
    :param board:
    :return: Hidden board for the player to solve
    """
    labeled_array, num_features = get_masked_array(board)
    to_mask_board = np.zeros(board.shape, dtype=int)
    for i in range(len(num_features)):
        for j in range(1, num_features[i] + 1):
            masked_matrix = (labeled_array[i] == j)
            indices = np.where(masked_matrix)
            to_keep = np.random.choice(range(len(indices[1])))
            to_mask_board[indices[0][to_keep], indices[1][to_keep]] = 1
    masked_board = board * to_mask_board
    return masked_board


def game(original_player_board, board, list_features):
    """
    This is the main interface function,
    This function calls the input functions, calls the validity function and
    game over function.
    It prints the outcome of the game - if the solution is correct, the game stops
    if not, it asks for prompt and starts a new input from the player
    :param original_player_board:
    :param board:
    :return: Outcome
    """
    player_board = copy.deepcopy(original_player_board)
    print("Starting board")
    print(player_board)

    # immutable cells - player cannot replace these cells
    fixed_cells = np.nonzero(player_board)
    fixed_cell_list = [(fixed_cells[0][i], fixed_cells[1][i]) for i in range(len(fixed_cells[0]))]
    while np.size(player_board) - np.count_nonzero(player_board) != 0:
        coord_added = input_coordinates()
        row, col, val = coord_added[0], coord_added[1], coord_added[2]
        # Check if the entered input is not in the fixed cell list
        if (row, col) in fixed_cell_list:
            print("This cell cannot be modified.. Please try again..")
        else:
            # Check if the entered value is continous
            if check_continuity(player_board, coord_added):
                if check_number_of_cells(player_board, coord_added):
                    player_board[row, col] = val
                    print("Player updated board")
                    print(player_board)
                else:
                    print("This number exceeds the allowed length for the region.. Please try again..")
            else:
                print("Continuity check failed, please try again")
    if check_board_valid(player_board, list_features):
        print("Congratulations, You have successfully solved the puzzle!!!")
    else:
        print("Sorry, your solution is incorrect")
        if click.confirm("Do you want to give it another try?"):
            game(original_player_board, board)



if __name__ == '__main__':
    num_rows, num_cols = game_level()
    board, list_features, iteration = generate_board(num_rows, num_cols)
    print("No. of iterations to generate the board = ", iteration)
    print('Board Generated = ')
    print(board)
    # num_rows, num_cols = 4, 4
    # board = np.array([[3, 3, 2, 2], [3, 1, 3, 3], [1, 4, 4, 3], [2, 2, 4, 4]])
    original_player_board = mask_board(board)
    game(original_player_board, board, list_features)
    # Todo currently, the game checks for solutions when all the empty cells are filled,
    #  however, if the player wants to change only couple of filled cells, it cannot happen after all cells are filled.
    #  Can work on another prompt - but need to modify the while loop in game function

