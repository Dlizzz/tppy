#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Name: tpsolutions.py       
    Description:
        talos-puzzle solution definition
"""
from PIL import Image, ImageDraw

# Class definition
class Solution(object):
    """Class: solution definition"""
    def __init__(self, pieces, board, tree_path):
        """Constructor: initialize the solution"""
        self.__board_columns = board.shape[1]
        self.__board_rows = board.shape[0]
        self.__solution_path = tree_path.copy()
        self.__solution_label = [["" for col in range(self.__board_columns)]
                                 for row in range(self.__board_rows)]
        self.__solution_pieces = [[0 for col in range(self.__board_columns)]
                                  for row in range(self.__board_rows)]
        for node in self.__solution_path:
            # If we have only one solution, solution is a tuple and not
            # a list of tuple
            if isinstance(node, tuple):
                piece_idx = node[0]
                position_idx = node[1]
            else:
                piece_idx = self.__solution_path[0]
                position_idx = self.__solution_path[1]
            position = (pieces[piece_idx].positions[position_idx])
            for row in range(self.__board_rows):
                for column in range(self.__board_columns):
                    if position[row][column] == 1:
                        self.__solution_label[row][column] = (pieces[
                                                              piece_idx].label)
                        self.__solution_pieces[row][column] = piece_idx

    def is_equal(self, solution):
        """Method: return true if teh given solution is equal to the current 
           solution (same solution label)
        """
        return (solution.label == self.__solution_label)

    def print_solution(self):
        """Method: print the solutiion on stdout"""
        print("Solution:\n--------", *self.__solution_label, sep="\n ")

    def draw_solution(self, cell_size, fill_color, shape_color):
        """Method: draw the solution with the given parameter"""
        # Create image with a drawing context
        image = Image.new("RGB", (self.__board_columns * cell_size,
                                  self.__board_rows * cell_size), fill_color)
        draw = ImageDraw.Draw(image)
        # Draw outside borders of pieces (use draw.line to have line
        # width)
        draw.line([(0, 0), (image.width - 1, 0)], shape_color, 2)
        draw.line([(image.width - 2, 0), (image.width - 2, image.height - 1)],
                  shape_color, 2)
        draw.line([(image.width - 1, image.height - 1), (0, image.height - 1)],
                  shape_color, 2)
        draw.line([(1, image.height - 1), (1, 0)], shape_color, 2)
        # Draw inside right borders of pieces
        for row in range(self.__board_rows):
            for col in range(self.__board_columns - 1):
                # Look on the right side of the cell and draw border
                # if cell on the right is different
                if (self.__solution_pieces[row][col] 
                    != self.__solution_pieces[row][col + 1]):
                    X0 = (col + 1) * cell_size - 1
                    Y0 = row * cell_size
                    X1 = X0
                    Y1 = (row + 1) * cell_size - 1
                    draw.line([(X0, Y0), (X1, Y1)], shape_color, 2)
        # Draw borders bellow pieces
        for row in range(self.__board_rows - 1):
            for col in range(self.__board_columns):
                # Look bellow the cell and draw border
                # if cell bellow is different
                if (self.__solution_pieces[row][col] 
                    != self.__solution_pieces[row + 1][col]):
                    X0 = col * cell_size
                    Y0 = (row + 1) * cell_size - 1
                    X1 = (col + 1) * cell_size - 1
                    Y1 = Y0
                    draw.line([(X0, Y0), (X1, Y1)], shape_color, 2)
        return image
