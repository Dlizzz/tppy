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
import copy
from PIL import ImageColor
from tppieces import Piece
from tpsolutions import Solution
from tppositions import combine_positions

# Class definition
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
        self.__images = None
        self.__cell_size = args.cell_size
        self.__fill_color = ImageColor.getrgb(args.fill_color)
        self.__shape_color = ImageColor.getrgb(args.shape_color)
        self.__output_dir = (args.output_dir 
                             + "\\Board {}Rx{}C - {}LR {}LL {}SR {}SL {}TE "
                             "{}BA {}SQ".format(args.rows, args.columns, 
                             args.l_right, args.l_left, args.step_right, 
                             args.step_left, args.tee, args.bar, args.square))
        # Game board dimensions
        self.__board_rows = args.rows
        self.__board_columns = args.columns
        # Stack of pieces with positions
        self.__pieces = []
        # Stack of solutions
        self.__solutions = []
        # Total combinations count
        self.__combinations_count = 1

    def __print_config(self):
        """Method: print puzzle configuration
        """
        print("Info: Puzzle board is {} rows x {} columns (size = {})"
              .format(self.__board_rows, self.__board_columns,
                      self.__board_rows * self.__board_columns))
        print("Info: Solving puzzle with the following pieces set:")
        for piece in self.__pieces:
            print("\t {} with {} positions"
                  .format(piece.name, len(piece.positions)))
        print("Info: Testing {:,d} combinations of positions"
              .format(self.__combinations_count).replace(",", " "))
        if self.__images:
            print("Info: Solutions image will be generated in {} with a cell "
                  "size of {}.".format(self.__images.output_dir,
                                       self.__images.cell_size))

    def add_piece(self, piece):
        """Method: add a piece, with all its possible positions on the board, 
           to the puzzle piece stack
        """
        # Add to piece stack
        self.__pieces.append(copy.deepcopy(piece))
        # Generate positions for the piece
        positions_count = (self.__pieces[-1]
                           .generate_positions(self.__board_rows,
                                               self.__board_columns))
        # Update the total count of combinations
        self.__combinations_count *= positions_count

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
        max_depth = len(self.__pieces) - 2
        if max_depth < 0 and self.__combinations_count > 0:
            # We have only one piece (a square or a bar) with one position
            # Then we have all the solutions
            board = numpy.zeros((self.__board_rows, self.__board_columns))
            tree_path = [(0, 0)]
            self.__solutions.append(Solution(self.__pieces, board, tree_path)) 
        else:
            # Sort the pieces stack from biggest number of positions to the
            # smallest, to optimize tree path
            self.__pieces.sort(key=lambda piece: len(piece.positions),
                               reverse=True)
            # Each position of the first piece is a tree root
            for position_idx in range(len(self.__pieces[0].positions)):
                # Init tree path with root node
                tree_path = [(0, position_idx)]
                # Init the board with root position
                board = numpy.copy(self.__pieces[0].positions[position_idx])
                # Recursively goes trough positions combination
                combine_positions(self.__pieces, self.__solutions, tree_path, 
                                  board, max_depth)
        stop = time.time()
        if self.__verbose:
            print("Info: Time spent in solving puzzle: {:,.2f} secondes"
                  .format(stop - start).replace(",", " "))

    def output_solutions(self):
        """Method: output the solutions if we have some"""
        # Remove duplicate solutions
        # TODO: Remove duplicate solutions
        # Report solutions
        if len(self.__solutions) != 0:
            print("Puzzle solved ! Found {} unique solutions"
                  .format(len(self.__solutions)))
            for solution in self.__solutions:
                solution.print_solution()
        else:
            print("No solution found for the puzzle !")
            exit(0)
        # Output images if needed
        if self.__images:
            # Create directory to store the images
            try:
                os.makedirs(self.__output_dir,exist_ok=True)
            except Exception as err:
                print("Fatal: Can\'t create output directory {}."
                      " System message is: "
                      .format(self.__output_dir), err)
                exit(1)
            # Draw and save all images
            for solution_idx, solution in enumerate(self.__solutions, 1):
                image = solution.draw_solution(self.__cell_size, 
                                               self.__fill_color, 
                                               self.__shape_color)
                image_name = (self.__output_dir + "\\Solution #{:0>2}.png"
                              .format(solution_idx))
                try:
                    image.save(image_name)
                except Exception as err:
                    print("Fatal: Can't save image {}. System message is: "
                          .format(image_name), err)
                    exit(1)
