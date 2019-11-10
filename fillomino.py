"""
Fillomino Puzzle solver and Generator

Authors: Gaurav Dharra, Harshitha Ravindra
"""

import numpy as np
import click

def generate_grid(num_rows, num_columns):
    """
    Method that generates a 2d numpy array with all zero values for given number of row and column values.
    :param num_rows: integer indicating number of rows
    :param num_columns: integer indicating number of rows
    :return: Returns a 2d array of the required size with all zeros
    """
    return np.zeros((num_rows, num_columns), int)



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


