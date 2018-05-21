#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Name: tpsolutions.py
    Description:
        talos-puzzle solution definition
"""

from PIL import Image, ImageDraw

from tperrors import ImageError


class SolutionsCollection(object):
    """Class: define a collection of solutions"""

    def __init__(self, positions, board_rows, board_columns):
        """Constructor: initialize the solutions stack"""
        # Stack of Solution
        self.__stack = []
        # Board dimensions
        self.__board_rows = board_rows
        self.__board_columns = board_columns
        # Positions collection
        self.__positions = positions

    def __len__(self):
        """Method: override len() method for the collection"""
        return len(self.__stack)

    def __getitem__(self, index):
        """Method: ovverride '[]' (indexer) operator for the collection"""
        return self.__stack[index]

    def __contains__(self, solution):
        """Method: override 'in' operator for the collection"""
        is_in = False
        for existing_solution in self.__stack:
            if solution == existing_solution:
                is_in = True
                break
        return is_in

    def add(self, tree_path):
        """Method: create and add a solution to the solutions stack, if not
           already exsiting. If solution alerady exists, do nothing.
        """
        solution = Solution(
            self.__positions,
            self.__board_rows,
            self.__board_columns,
            tree_path
        )
        # Check if solutioin already existing, and drops it if yes
        # Not already in the stack, add it
        if solution not in self.__stack:
            self.__stack.append(solution)

    def echo(self):
        """Method: print the solutiions on stdout"""
        for solution_idx, solution in enumerate(self.__stack, 1):
            print("Solution {}:".format(solution_idx), solution, sep="\n")

    def draw(self, cell_size, fill_color, shape_color):
        """Method: draw all solutions as PNG images"""
        for solution in self.__stack:
            solution.draw(cell_size, fill_color, shape_color)

    def save(self, output_dir):
        """Method: save all solutions as PNG images, in the given directory.
            Raise ImageException if saving fails.
        """
        # Save all images
        for solution_idx, solution in enumerate(self.__stack, 1):
            # Image filename
            image_name = (
                output_dir
                / "Solution #{:0>2}.png".format(solution_idx)
            )
            if solution.image:
                try:
                    solution.image.save(str(image_name))
                except Exception as err:
                    message = "Fatal: Can't save image {}".format(
                        str(image_name)
                    )
                    raise ImageError(message, err)


class Solution(object):
    """Class: solution definition"""

    def __init__(self, positions, board_rows, board_columns, tree_path):
        """Constructor: initialize the solution"""
        self.__image = None
        self.__board_rows = board_rows
        self.__board_columns = board_columns
        self.__solution_path = tree_path.copy()
        self.__solution_label = [
            ["" for col in range(self.__board_columns)]
            for row in range(self.__board_rows)
        ]
        self.__solution_pieces = [
            [0 for col in range(self.__board_columns)]
            for row in range(self.__board_rows)
        ]
        for node in self.__solution_path:
            # If we have only one solution, solution_path is a tuple and not
            # a list of tuple
            if isinstance(self.__solution_path, tuple):
                piece_idx = self.__solution_path[0]
                position_idx = self.__solution_path[1]
            else:
                piece_idx = node[0]
                position_idx = node[1]
            position = (positions[piece_idx][position_idx])
            for row in range(self.__board_rows):
                for column in range(self.__board_columns):
                    if position[row][column] == 1:
                        self.__solution_label[row][column] = (
                            positions[piece_idx].piece.label
                        )
                        self.__solution_pieces[row][column] = piece_idx

    def __str__(self):
        """Method: ovveride to string method for the object"""
        solution_str = ""
        for row in range(self.__board_rows):
            solution_str += "|" + " ".join(self.__solution_label[row]) + "|\n"
        return solution_str

    def __eq__(self, other):
        """ Method: ovveride equality. Solutions are equal if both 
            solution_label (including symmetrical solutions) are equal.
        """
        solution_label = other.solution_label
        # Vertical symmetry
        fv_solution_label = other.solution_label[::-1]
        # Horizontal symmetry
        fh_solution_label = [x[::-1] for x in other.solution_label]
        # Central symmetry
        fhv_solution_label = fh_solution_label[::-1] 
        return (
            solution_label == self.__solution_label
            or fv_solution_label == self.__solution_label
            or fh_solution_label == self.__solution_label
            or fhv_solution_label == self.__solution_label
        )

    @property
    def image(self):
        """Property: png image (PIL image) of the solution."""
        return self.__image

    @property
    def path(self):
        """Property: solution path."""
        return self.__solution_path

    @property
    def solution_label(self):
        """Property: solution with the pieces labels."""
        return self.__solution_label

    @property
    def solution_pieces(self):
        """Property: solution with the pieces number"""
        return self.__solution_pieces

    def draw(self, cell_size, fill_color, shape_color):
        """Method: draw the solution with the given parameter."""
        # Create image with a drawing context
        self.__image = Image.new(
            "RGB", (
                self.__board_columns * cell_size,
                self.__board_rows * cell_size
            ),
            fill_color
        )
        draw = ImageDraw.Draw(self.__image)
        # Draw outside borders of pieces (use draw.line to have line
        # width)
        width = self.__image.width
        height = self.__image.height
        draw.line([(0, 0), (width - 1, 0)], shape_color, 2)
        draw.line([(width - 2, 0), (width - 2, height - 1)], shape_color, 2)
        draw.line([(width - 1, height - 1), (0, height - 1)], shape_color, 2)
        draw.line([(1, height - 1), (1, 0)], shape_color, 2)
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
