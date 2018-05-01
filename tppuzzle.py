#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Name: tppuzzle.py       
    Description:
        talos-puzzle puzzle definition
"""
import numpy
import copy
import tppieces
import progress

# Class definition
class Combination(object):
    """Class: define a combination of positions, keeping history of 
       construction and status as a valid combination or not"""
    def __init__(self, position, combination = None):
        """Constructor: initialize the combination by adding position to 
           existing given combination, if it exists"""
        # Public members
        if combination is None:
            # No initial combination, so start with position
            self.board = numpy.copy(position.board)
            self.combined_positions = [position.index]
        else:
            # Copy given combination
            self.board = numpy.copy(combination.board)
            # Add position to combination
            self.board += position.board
            # Copy combination history
            self.combined_positions = copy.deepcopy(combination
                                                    .combined_positions)
            # Add position to history
            self.combined_positions.append(position.index)
        # Is it a valid position ?
        self.isvalid = numpy.max(self.board) <= 1
    
class Puzzle(object):
    """Class: game board and stack of solutions"""
    def __init__(self, rows=0, columns=0, verbose=False):
        """Constructor: create board with rows x columns dimension"""
        # Protected members
        # Do we have to be verbose
        self.__verbose = verbose
        # Game board dimensions
        self.__board_rows = rows
        self.__board_columns = columns
        # Stack of pieces with positions
        self.__pieces = []
        # Stack of stack of combinations (by pieces then combinations)
        self.__combinations = []
        # Number of positions combinations
        self.__total_combinations = 1
        if self.__verbose:
            print("Info: Create puzzle with {} rows and {} columns."
                  .format(rows, columns))
            print("Info: Board size is {}.".format(rows*columns))
  
    def add_piece(self, piece):
        """Method: add a piece, with all its possible positions on the board, 
        to the puzzle piece stack"""
        # Add to piece stack
        self.__pieces.append(copy.deepcopy(piece))
        # Generate positions for the piece
        self.__pieces[-1].generate_positions(len(self.__pieces) - 1, 
                                             self.__board_rows, 
                                             self.__board_columns)        
        # Update the total number of combinations
        self.__total_combinations *= len(self.__pieces[-1].positions)
        if self.__verbose:
            print("Info: Adding {} positions for piece '{}'"
                  .format(len(self.__pieces[-1].positions), 
                          self.__pieces[-1].name))    

    def solve(self):
        """Method: solve the puzzle by going trhough all combinations of pieces
           positions"""
        if self.__verbose:
            print("Info: testing {} combinations of positions in total !"
                  .format(self.__total_combinations))
        # Start with first piece, with no previous combination
        # Add a new stack of combinations
        self.__combinations.append([])
        combination_count = 0
        for position in self.__pieces[0].positions:
            self.__combinations[0].append(Combination(position))
            combination_count += 1
            progress.progress(combination_count, self.__total_combinations,
                              "Piece 1 on {}: {} combinations done"
                              .format(len(self.__pieces), combination_count))
        # Continue with the rest of pieces
        for piece_idx in range(1, len(self.__pieces)):
            # Add a new stack of combinations
            self.__combinations.append([])
            # Go through all previous combinations
            for combination in self.__combinations[piece_idx - 1]:
                # Combine each previous combination with all positions of piece
                # only if it's a valid combination
                if combination.isvalid:
                    for position in self.__pieces[piece_idx].positions:
                        self.__combinations[piece_idx].append(Combination(
                                                              position, 
                                                              combination))
                combination_count += len(self.__pieces[piece_idx].positions)
                progress.progress(combination_count, self.__total_combinations,
                                  "Piece {} on {}: {} combinations done"
                                  .format(piece_idx + 1, len(self.__pieces), 
                                  combination_count))
        print("")        
    
    def output_solutions(self):
        """Method: output the solutions if we have some"""
        # Report solutions (valid combinations for last piece)
        for combination in self.__combinations[-1]:
            if combination.isvalid:
                for p in combination.combined_positions:
                    print(self.__pieces[p.piece].positions[p.position].board)
                    print("----")