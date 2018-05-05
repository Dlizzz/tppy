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
import tppieces

# Class definition
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
        # Combinations count
        self.__combinations_count = 1
        # Solutions
        self.__solutions = []
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
        self.__pieces[-1].generate_positions(self.__board_rows, 
                                             self.__board_columns)        
        # Update the total count of combinations
        positions_count = len(self.__pieces[-1].positions)
        self.__combinations_count *= positions_count
        if self.__verbose:
            print("Info: Adding {} positions for piece '{}'"
                  .format(positions_count, self.__pieces[-1].name))    

    def solve(self):
        """Method: solve the puzzle by going trhough all combinations of pieces
           positions. Combination is a tuple (board, isvalid, position1, 
           position2, ...) with one position per piece"""
        if self.__verbose:
            print("Info: testing {:,d} combinations of positions in total !"
                  .format(self.__combinations_count).replace(",", " "))
        # Add a new stack of combinations
        # Start with first piece, with no previous combination, all 
        # combinations are valid
        start = time.time()
        self.__combinations.append([])
        for position_idx, position in enumerate(self.__pieces[0].positions):
            board = numpy.copy(position)
            self.__combinations[0].append((board, True, position_idx))
        # Continue with the rest of pieces
        for piece_idx in range(1, len(self.__pieces)):
            # Add a new stack of combinations
            self.__combinations.append([])
            # Go through all previous combinations
            for combination in self.__combinations[piece_idx - 1]:
                # Combine each previous combination with all positions of piece
                # only if it's a valid combination
                if combination[1]:
                    # Combination is valid
                    for position_idx, position in (enumerate(
                                                   self.__pieces[piece_idx]
                                                   .positions)):
                        # Copy the previous combination
                        board = numpy.copy(combination[0])
                        # Add the current position
                        board += position
                        # Test if valid combination
                        isvalid = (numpy.max(board) <= 1)
                        # Add position index to the list
                        combination_new = ((board, isvalid) + combination[2:]
                                          + (position_idx,))
                        self.__combinations[piece_idx].append(combination_new)
        stop = time.time()
        if self.__verbose:
            print("Info: Time spent in solving puzzle: {:,.2f} secondes"
                  .format(stop - start).replace(",", " "))
    
    def solutions(self):
        """Method: output the solutions if we have some"""
        # Report solutions (valid combinations for last piece)
        for combination in self.__combinations[-1]:
            if combination[1]:
                # Combination is valid, that's a solution
                solution = [["" 
                            for col 
                            in range(self.__board_columns)] 
                            for row 
                            in range(self.__board_rows)]
                for piece_idx, piece in enumerate(self.__pieces):
                    # Get the position for each piece, sequentially stored in
                    # combination, starting at element 3
                    position_idx = combination[piece_idx + 2]
                    for row in range(self.__board_rows):
                        for col in range(self.__board_columns): 
                            if piece.positions[position_idx][row][col] == 1:
                                solution[row][col] = piece.label
                if solution not in self.__solutions:
                    self.__solutions.append(solution)
                    print('Solution:', *solution, sep='\n ')
                    print("----")