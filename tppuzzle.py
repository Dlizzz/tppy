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
        self.__solutions = [] 
        # Solutions with label to remove duplicates
        self.__solutions_label = []
        # Solutions with pieces index to draw solution
        self.__solutions_pieces = []
        # Total combinations count
        self.__combinations_count = 1
  
    def add_piece(self, piece):
        """Method: add a piece, with all its possible positions on the board, 
        to the puzzle piece stack"""
        # Add to piece stack
        self.__pieces.append(copy.deepcopy(piece))
        # Generate positions for the piece
        self.__pieces[-1].generate_positions(self.__board_rows, 
                                             self.__board_columns)        
        # Update the total count of combinations
        positions_count = len(self.__pieces[-1].positions)
        self.__combinations_count *= positions_count
        if self.__verbose:
            print("Info: Adding {} positions for piece '{}'"
                  .format(positions_count, self.__pieces[-1].name))    

    def solve(self):
        """Method (public): 
           Solve the puzzle by going trhough all combinations of pieces
           positions, moving horizontally in the tree, i.e. each time we have a
           valid combination for a piece, test it with the next piece 
           positions.
        """
        if self.__verbose:
            print("Info: Solve puzzle with {} rows and {} columns. Board size "
                  "is {}".format(self.__board_rows, self.__board_columns,
                  self.__board_rows * self.__board_columns))
            print("Info: Testing {:,d} combinations of positions in total !"
                  .format(self.__combinations_count).replace(",", " "))
        start = time.time()
        # Maximum depth to reach in the tree (one level before the last one) 
        max_depth = len(self.__pieces) - 2 
        if max_depth < 0:
            # We have only one piece (a square or a bar) with one position
            # Then we have all the solutions
            self.__solutions.append((0, 0))
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
            print()
            print("Info: Time spent in solving puzzle: {:,.2f} secondes"
                  .format(stop - start).replace(",", " "))

    def solutions(self):
        """Method: output the solutions if we have some"""
        # Output solutions       
        for solution in self.__solutions:
            solution_label = [["" 
                               for col in range(self.__board_columns)] 
                               for row in range(self.__board_rows)]
            solution_pieces = [[0 
                                for col in range(self.__board_columns)] 
                                for row in range(self.__board_rows)]
            for node in solution:
                position = (self.__pieces[node[0]].positions[node[1]])
                for row in range(self.__board_rows):
                    for column in range(self.__board_columns):
                        if position[row][column] == 1:
                            solution_label[row][column] = self.__pieces[
                                                          node[0]].label
                            solution_pieces[row][column] = node[0]
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
        if not self.__images is None:
            if self.__verbose:
                print("Info: Solutions image will be generated in {} "
                      "with a cell size of {}."
                      .format(self.__images.output_dir, 
                              self.__images.cell_size))
            for solution_idx, solution in enumerate(self.__solutions_pieces, 
                                                   1):
                try:
                    self.__images.output_solution(solution_idx, solution)
                except ImagesError as err:
                    print(err.message)
                    exit(1)
