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
    game_option = click.prompt('Please select grid size: \n \
         Enter 1 for (10 X 5) \n  \
         Enter 2 for  (10 X 10)' , type=click.IntRange(1, 2))

    game_difficulty = click.prompt('Please select difficulty level: \n \
        Enter 1 for easy \n  \
        Enter 2 for medium \n \
        Enter 3 for difficult', type=click.IntRange(1, 3))

    if game_option == 1:
        m = 10
        n = 5
    else:
        m = 10
        n = 10

    return m, n, game_difficulty

#Marking this to be removed
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
    try:
        input_coord = [int(x) for x in val]
    except Exception:
        print("Wrong input, try again")
        return input_coordinates()
    if len(input_coord) != 3:
        print("Wrong input, try again")
        return input_coordinates()
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
    if np.count_nonzero(cloned_board) == cloned_board.size:
        label_to_be_verified = labeled_board[val-1]
    else:
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


def mask_board(board, level):
    """
    This function takes the generated board and hides elements and creates a puzzle for the
    player to solve.
    For every type of number, only 1 element is displayed. for example if the board is [[1,2,2],[2,3,3],[2,1,3]]
    [[1,2,0],[0,3,0],[2,1,0]] is created.
    :param board:
    :param level:
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

    number_of_hints = 6 if level == 1 else 3

    if level != 3:
        zero_coord = np.where(masked_board == 0)
        list_zero_coord = [[zero_coord[0][i],zero_coord[1][i]] for i in range(len(zero_coord[0]))]
        chosen_zero_coord = random.sample(list_zero_coord, number_of_hints)
        for [i, j] in chosen_zero_coord:
            masked_board[i][j] = board[i][j]

    board_to_be_displayed = copy.deepcopy(masked_board)

    if level == 2:
        board_to_be_displayed = np.array(board_to_be_displayed, dtype=object)
        randomly_choosing_point_to_mask = random.choice(chosen_zero_coord)
        number_to_be_masked = board_to_be_displayed[randomly_choosing_point_to_mask[0]][randomly_choosing_point_to_mask[1]]
        feature_number = labeled_array[number_to_be_masked-1][randomly_choosing_point_to_mask[0]][randomly_choosing_point_to_mask[1]]
        feature_coordinates = np.where(labeled_array[number_to_be_masked-1] == feature_number)
        list_feature_coordinates = [[feature_coordinates[0][i], feature_coordinates[1][i]] for i in range(len(feature_coordinates[0]))]

        list_feature_coordinates.remove(randomly_choosing_point_to_mask)

        for [i, j] in list_feature_coordinates:
            if board_to_be_displayed[i][j] != 0:

                board_to_be_displayed[i][j] = 'X'
                board_to_be_displayed[randomly_choosing_point_to_mask[0]][randomly_choosing_point_to_mask[1]] = 'X'
                break

    return masked_board, board_to_be_displayed



def display_board(board):
    """
    :param board:
    :return:
    """
    print("   ", "   ".join([str(x) for x in range(board.shape[1])]))
    # print(" ", "".join(['----' for x in range(board.shape[1])]))
    for i, x in enumerate(board):
        print(i, ":", " ".join([str(y)+' |' for y in x]))


def game(original_player_board, displaying_board, board, list_features):
    """
    This is the main interface function,
    This function calls the input functions, calls the validity function and
    game over function.
    It prints the outcome of the game - if the solution is correct, the game stops
    if not, it asks for prompt and starts a new input from the player
    :param original_player_board:
    :param displaying_board:
    :param board:
    :return: Outcome
    """
    # player_board = copy.deepcopy(original_player_board)
    player_board = copy.deepcopy(displaying_board)
    print("Starting board")
    display_board(player_board)

    player_board_to_be_checked = copy.deepcopy(original_player_board)

    board_shape = player_board_to_be_checked.shape

    # immutable cells - player cannot replace these cells
    fixed_cells = np.nonzero(player_board)
    fixed_cell_list = [(fixed_cells[0][i], fixed_cells[1][i]) for i in range(len(fixed_cells[0])) if player_board[fixed_cells[0][i]][fixed_cells[1][i]] != 'X']
    while np.size(player_board) - np.count_nonzero(player_board) != 0:
        coord_added = input_coordinates()
        row, col, val = coord_added[0], coord_added[1], coord_added[2]
        # Check if the entered input is not in the fixed cell list
        if row < 0 or row >= board_shape[0] or col < 0 or col >= board_shape[1]:
            print("The input coordinate entered is outside board size. Please try again..")
        elif (row, col) in fixed_cell_list:
            print("This cell cannot be modified.. Please try again..")
        else:
            # Check if the entered value is continous
            if check_continuity(player_board_to_be_checked, coord_added):
                if check_number_of_cells(player_board_to_be_checked, coord_added):
                    player_board[row, col] = val
                    player_board_to_be_checked[row, col] = val
                    print("Player updated board")
                    display_board(player_board)
                else:
                    print("This number exceeds the allowed length for the region.. Please try again..")
            else:
                print("Continuity check failed, please try again")
    if check_board_valid(player_board_to_be_checked, list_features):
        print("Congratulations, You have successfully solved the puzzle!!!")
    else:
        print("Sorry, your solution is incorrect")
        if click.confirm("Do you want to give it another try?"):
            game(original_player_board, board)


ten_board = np.array([[8, 8, 8, 8, 1, 5, 5, 5, 9, 9],
                      [8, 1, 8, 8, 6, 6, 5, 5, 9, 9],
                      [3, 3, 1, 8, 1, 6, 6, 9, 9, 1],
                      [3, 1, 9, 9, 9, 6, 6, 9, 9, 2],
                      [9, 9, 9, 9, 9, 9, 1, 9, 1, 2],
                      [1, 4, 4, 4, 1, 4, 4, 1, 7, 7],
                      [9, 9, 1, 4, 7, 1, 4, 4, 7, 7],
                      [9, 9, 9, 7, 7, 2, 7, 7, 7, 1],
                      [1, 9, 9, 7, 7, 2, 6, 6, 6, 6],
                      [9, 9, 1, 7, 7, 1, 6, 1, 6, 1]])


def generate_ten_board(board10):
    """
     https://stackoverflow.com/questions/16856788/slice-2d-array-into-smaller-2d-arrays
     https://stackoverflow.com/questions/32838802/numpy-with-python-convert-3d-array-to-2d
    :param board10:
    :return:
    """
    original_board10 = copy.deepcopy(board10)
    unique, counts = np.unique(board10, return_counts=True)
    list_features_2d = [[x] * x for idx, x in enumerate(unique) for i in range(counts[idx] // x)]
    list_features = [j for i in list_features_2d for j in i]
    board100 = original_board10.reshape(5, 2, -1, 2).swapaxes(1, 2).reshape(-1, 2, 2)
    grid_valid = False
    iter_val = 0
    while (not grid_valid) | iter_val < 10000:
        split_board = copy.deepcopy(board100)
        random.shuffle(split_board)
        result_board = split_board.transpose(2, 0, 1).reshape(10, -1)
        grid_valid = check_board_valid(result_board, list_features)
        iter_val += 1

    if iter_val == 10000:
        to_rot = random.randint(1, 4)
        return np.rot90(board10, to_rot), list_features

    return result_board, list_features


if __name__ == '__main__':
    num_rows, num_cols, level = game_level()
    if num_cols == 5:
        board, list_features, iteration = generate_board(num_rows, num_cols)
        print("No. of iterations to generate the board = ", iteration)
    else:
        board, list_features = generate_ten_board(ten_board)
    print('Board Generated = ')
    print(board)

    # num_rows, num_cols = 4, 4
    # board = np.array([[3, 3, 2, 2], [3, 1, 3, 3], [1, 4, 4, 3], [2, 2, 4, 4]])
    original_player_board, board_to_be_displayed = mask_board(board, level)
    game(original_player_board, board_to_be_displayed, board, list_features)

