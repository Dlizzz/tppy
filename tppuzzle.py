#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Name: tppuzzle.py
    Description:
        talos-puzzle puzzle definition
"""
import os
import numpy
import time
from PIL import ImageColor
from tpsolutions import SolutionsCollection
from tppieces import PiecesCollection
from tperrors import ImageError
from tppositions import combine_positions


class Puzzle(object):
    """Class: game board and stack of solutions"""

    def __init__(self, args):
        """Constructor: init the puzzle with rows x columns dimension"""
        # Protected members
        # Do we have to be verbose
        self.__verbose = args.verbose
        # Do we stop at first solution found
        self.__first = args.first
        # Images output
        self.__save_images = args.images
        self.__cell_size = args.cell_size
        self.__fill_color = ImageColor.getrgb(args.fill_color)
        self.__shape_color = ImageColor.getrgb(args.shape_color)
        self.__output_dir = (
            args.output_dir
            + "\\Board {}Rx{}C - {}LR {}LL {}SR {}SL {}TE {}BA {}SQ"
            .format(
                args.rows,
                args.columns,
                args.l_right,
                args.l_left,
                args.step_right,
                args.step_left,
                args.tee,
                args.bar,
                args.square
            )
        )
        # Stack of pieces with positions
        self.__pieces = PiecesCollection()
        # Collection of solutions
        self.__solutions = SolutionsCollection()
        # Properties (read only)
        # Game board dimensions
        self._board_rows = args.rows
        self._board_columns = args.columns
        # Total combinations count
        self._combinations_count = 1

    @property
    def board_rows(self):
        return self._board_rows

    @property
    def board_columns(self):
        return self._board_columns

    @property
    def combinations_count(self):
        return self._combinations_count

    def __print_config(self):
        """Method: print puzzle configuration"""
        print(
            "Info: Puzzle board is {} rows x {} columns (size = {})"
            .format(
                self._board_rows,
                self._board_columns,
                self._board_rows * self._board_columns
            )
        )
        print("Info: Solving puzzle with the following pieces set:")
        for piece in self.__pieces.stack:
            print("\t {} with {} positions"
                  .format(piece.name, len(piece.positions)))
        print("Info: Testing {:,d} combinations of positions"
              .format(self._combinations_count).replace(",", " "))
        if self.__save_images:
            print("Info: Solutions image will be generated in {} with a cell "
                  "size of {}.".format(self.__output_dir, self.__cell_size))

    def add_piece(self, piece):
        """Method: add a piece, with all its possible positions on the board,
           to the puzzle piece stack
        """
        # Add to piece stack
        positions_count = self.__pieces.add(
            piece,
            self._board_rows,
            self._board_columns
        )
        # Update the total count of combinations
        self._combinations_count *= positions_count

    def solve(self):
        """Method (public):
           Solve the puzzle by going trhough all combinations of pieces
           positions, moving horizontally in the tree, i.e. each time we have a
           valid combination for a piece, test it with the next piece
           positions.
        """
        # Print config if needed
        if self.__verbose:
            self.__print_config()
        start = time.time()
        # Maximum depth to reach in the tree (one level before the last one)
        max_depth = self.__pieces.count - 2
        if max_depth < 0 and self._combinations_count > 0:
            # We have only one piece (a square or a bar) with one position
            # Then we have all the solutions
            self.__solutions.add(
                self.__pieces,
                self._board_rows,
                self._board_columns,
                [(0, 0)]
            )
        else:
            # Sort the pieces stack from biggest number of positions to the
            # smallest, to optimize tree path
            self.__pieces.sort()
            # Each position of the first piece is a tree root
            for position_idx in range(len(self.__pieces.stack[0].positions)):
                # Init tree path with root node
                tree_path = [(0, position_idx)]
                # Init the board with root position
                board = numpy.copy(
                    self.__pieces.stack[0].positions[position_idx]
                )
                # Recursively goes trough positions combination
                combine_positions(
                    self.__pieces,
                    self.__solutions,
                    tree_path,
                    board,
                    max_depth
                )
        stop = time.time()
        if self.__verbose:
            print("Info: Time spent in solving puzzle: {:,.2f} secondes"
                  .format(stop - start).replace(",", " "))

    def solutions(self):
        """Method: output the solutions if we have some"""
        # Report solutions
        if self.__solutions.count != 0:
            print("Puzzle solved ! Found {} unique solutions"
                  .format(self.__solutions.count))
            self.__solutions.echo()
        else:
            print("No solution found for the puzzle !")
            exit(0)
        # Save images if needed
        if self.__save_images:
            # Create directory to store the images
            try:
                os.makedirs(self.__output_dir, exist_ok=True)
            except OSError as err:
                print("Fatal: Can\'t create output directory {}."
                      " System message is: "
                      .format(self.__output_dir), err)
                exit(1)
            # Draw all solutions
            self.__solutions.draw(self.__cell_size, self.__fill_color,
                                  self.__shape_color)
            # Save all solutions
            try:
                self.__solutions.save(self.__output_dir)
            except ImageError as err:
                print(err.message, " with system error: ", err.syserror)
                exit(1)
