#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Name: tppuzzle.py       
    Description:
        talos-puzzle puzzle definition
"""
import numpy
import time
import copy
from tppieces import Piece
from tpimages import Images, ImagesError
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
        if args.images:
            self.__images = Images(args)
        # Game board dimensions
        self.__board_rows = args.rows
        self.__board_columns = args.columns
        # Stack of pieces with positions
        self.__pieces = []
        # Solution nodes, stack of stack of valid tree path
        self.__solutions_paths = []
        # Solutions with label to remove duplicates
        self.__solutions_label = []
        # Solutions with pieces index to draw solution
        self.__solutions_pieces = []
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
            self.__solutions_paths.append((0, 0))
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
                combine_positions(self.__pieces, self.__solutions_paths,
                                  tree_path, board, max_depth)
        stop = time.time()
        if self.__verbose:
            print("Info: Time spent in solving puzzle: {:,.2f} secondes"
                  .format(stop - start).replace(",", " "))

    def solutions(self):
        """Method: output the solutions if we have some"""
        # Output solutions
        for solution in self.__solutions_paths:
            solution_label = [[""
                               for col in range(self.__board_columns)]
                              for row in range(self.__board_rows)]
            solution_pieces = [[0
                                for col in range(self.__board_columns)]
                               for row in range(self.__board_rows)]
            for node in solution:
                if isinstance(node, tuple):
                    piece_idx = node[0]
                    position_idx = node[1]
                else:
                    # If we have only one solution, solution is a tuple and not
                    # a list of tuple 
                    piece_idx = solution[0]
                    position_idx = solution[1]                    
                position = (self.__pieces[piece_idx].positions[position_idx])
                for row in range(self.__board_rows):
                    for column in range(self.__board_columns):
                        if position[row][column] == 1:
                            solution_label[row][column] = (self.__pieces[
                                                           piece_idx].label)
                            solution_pieces[row][column] = piece_idx
            if solution_label not in self.__solutions_label:
                # Add solution if not already existing
                self.__solutions_label.append(solution_label)
                self.__solutions_pieces.append(solution_pieces)
                print("Solution:\n--------", *solution_label, sep="\n ")
        # Report solutions
        if len(self.__solutions_label) != 0:
            print("Puzzle solved ! Found {} unique solutions"
                  .format(len(self.__solutions_label)))
        else:
            print("No solution found for the puzzle !")
            exit(0)
        # Output images if needed
        if self.__images:
            for solution_idx, solution in enumerate(self.__solutions_pieces,
                                                    1):
                try:
                    self.__images.output_solution(solution_idx, solution)
                except ImagesError as err:
                    print(err.message)
                    exit(1)
