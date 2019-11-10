"""
Fillomino Puzzle solver and Generator

Authors: Gaurav Dharra, Harshitha Ravindra
"""

import numpy as np


def generate_grid(num_rows, num_columns):
    """
    Method that generates a 2d numpy array with all zero values for given number of row and column values.
    :param num_rows: integer indicating number of rows
    :param num_columns: integer indicating number of rows
    :return: Returns a 2d array of the required size with all zeros
    """
    return np.zeros((num_rows, num_columns), int)


