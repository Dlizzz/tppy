#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Define Solution and SolutionsCollection

Name: tpsolutions.py
Classes:
    SolutionsCollection: collection of Solutions - solutions of the puzzle
    Solution: solution description
Dependencies:
    PIL
    tperrors
"""


from PIL import Image, ImageDraw

from tperrors import TalosFileSystemError


class SolutionsCollection(object):
    """Define a collection of solutions of the puzzle

    Public members:
        Methods:
            add: create and append a solution to the collection
            echo: output all solutions on the console
            draw: generate PNG images of all solutions
            save: generated PNG images
    Private members:
        Attributes:
            __stack: list of Solution - store the solutions
            __positions: collections of PositionsStack - positions tree
            __board_rows: integer - # rows of the puzzle
            __board_columns: integer - # columns of the puzzle
    Special methods:
        __init__: override object constructor
        __len__: provide len method, # of items in the collection
        __getitem__: provide 'indexer' ([]) operator, collection is iterable
        __contains__: provide the 'in' for the collection
    Exceptions:
        TalosFileSystemError: error in saving images
    """

    def __init__(self, positions, board_rows, board_columns):
        """Override object constructor

        Inputs:
            positions: PositionsStackCollection - puzzle collection of
                positions
            board_rows: integer - # rows of the puzzle
            board_columns: integer - # columns of the puzzle
        """

        # Stack of Solution
        self.__stack = []
        # Board dimensions
        self.__board_rows = board_rows
        self.__board_columns = board_columns
        # Positions collection
        self.__positions = positions

    def __len__(self):
        """Provide len method, # of items in the collection

        Return: integer - # items in the collection
        """

        return len(self.__stack)

    def __getitem__(self, index):
        """Provide [] operator, collection is iterable

        Inputs:
            index: integer - index of the requested item
        Return: Piece - the requested piece
        """

        return self.__stack[index]

    def __contains__(self, solution):
        """Provide in operator

        Inputs:
            solution: Solution - the solution to test
        Return: boolean - True if given solution is in the collection
        """

        is_in = False
        for existing_solution in self.__stack:
            if solution == existing_solution:
                is_in = True
                break
        return is_in

    def add(self, tree_path):
        """Create and append a solution to the solutions stack, if not
           already exsiting. If solution alerady exists, do nothing.

        Inputs:
            tree_path: list of tupples (row, column) - a valid tree_path
                representing the solution
        """

        solution = Solution(
            self.__positions,
            self.__board_rows,
            self.__board_columns,
            tree_path
        )
        # Not already in the stack, add it
        if solution not in self.__stack:
            self.__stack.append(solution)

    def echo(self):
        """Output the solutions on stdout"""

        for solution_idx, solution in enumerate(self.__stack, 1):
            print("Solution {}:".format(solution_idx), solution, sep="\n")

    def draw(self, cell_size, fill_color, shape_color):
        """Draw all solutions as PNG images

        Inputs:
            cell_size: integer - side lenght in pixels of one square cell
            fill_color: rgb tuple of integer - color of the cell
            shape_color rgb tuple of integer - color of the shape of the cell
        """

        for solution in self.__stack:
            solution.draw(cell_size, fill_color, shape_color)

    def save(self, output_dir):
        """Save all solutions as PNG images, in the given directory.

        Inputs:
            output_dir: string - directory where to save the images
        Exceptions:
            TalosFileSystemError - error in saving images
        """

        # Save all images
        for solution_idx, solution in enumerate(self.__stack, 1):
            if solution.image:
                # Image filename
                image_name = (
                    output_dir
                    / "Solution #{:0>2}.png".format(solution_idx)
                )
                try:
                    solution.image.save(str(image_name))
                except Exception as err:
                    message = "Can't save image {}".format(str(image_name))
                    raise TalosFileSystemError(message, err)


class Solution(object):
    """Solution definition

    Public members:
        Methods:
            draw: draw the solution as PNG image
    Private members:
        Attributes:
            __image: Image (PIL) - the image of the solution
            __board_rows: integer - # of rows in the puzzle
            __board_columns: integer - # of columns in the puzzle
            __solution_path: list of integer tuples (row, column) - valid tree
                path of the solution
            __solution_label: list of list of string - the solution with label
                of pieces
            __solutions_pieces: list of list of integer - the solution with
                index of pieces
    Special methods:
        __init__: override object constructor
        __str__: the solution in a string
        __eq__: implement equality for two solutions
    Properties:
        image: Image (PIL) - the image of the solution
        path: list of integer tuples (row, column) - valid tree path of the
            solution
        solution_label: list of list of string - the solution with label of
            pieces
        solutions_pieces: list of list of integer - the solution with index of
            pieces
    """

    def __init__(self, positions, board_rows, board_columns, tree_path):
        """Initialize the solution

        Inputs:
            positions: PositionsStackCollection - puzzle collection of
                positions
            board_rows: integer - # rows of the puzzle
            board_columns: integer - # columns of the puzzle
            tree_path: list of integer tuples (row, column) - valid tree path
                of the solution
        """
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
        """Ovveride to string method for the object

        Return: string - the solution as a string
        """

        solution_str = ""
        for row in range(self.__board_rows):
            solution_str += "|" + " ".join(self.__solution_label[row]) + "|\n"
        return solution_str

    def __eq__(self, other):
        """Provide equality. Solutions are equal if both
            solution_label (including symmetrical solutions) are equal.

        Return: boolean - True if solutions are equal
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
        """Image (PIL) - PNG image of the solution."""

        return self.__image

    @property
    def path(self):
        """List of integer tuples (row, col) - solution path"""

        return self.__solution_path

    @property
    def solution_label(self):
        """List of list of string - solution with the pieces label"""

        return self.__solution_label

    @property
    def solution_pieces(self):
        """List of list of integer - solution with the pieces index"""

        return self.__solution_pieces

    def draw(self, cell_size, fill_color, shape_color):
        """Draw all solutions as PNG images

        Inputs:
            cell_size: integer - side lenght in pixels of one square cell
            fill_color: rgb tuple of integer - color of the cell
            shape_color rgb tuple of integer - color of the shape of the cell
        """

        # Create image with a drawing context
        self.__image = Image.new(
            "RGB",
            (
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
                if (
                    self.__solution_pieces[row][col]
                    != self.__solution_pieces[row][col + 1]
                ):
                    x0 = (col + 1) * cell_size - 1
                    y0 = row * cell_size
                    x1 = x0
                    y1 = (row + 1) * cell_size - 1
                    draw.line([(x0, y0), (x1, y1)], shape_color, 2)
        # Draw borders bellow pieces
        for row in range(self.__board_rows - 1):
            for col in range(self.__board_columns):
                # Look bellow the cell and draw border
                # if cell bellow is different
                if (
                    self.__solution_pieces[row][col]
                    != self.__solution_pieces[row + 1][col]
                ):
                    x0 = col * cell_size
                    y0 = (row + 1) * cell_size - 1
                    x1 = (col + 1) * cell_size - 1
                    y1 = y0
                    draw.line([(x0, y0), (x1, y1)], shape_color, 2)
