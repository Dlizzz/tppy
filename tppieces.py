#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Name: tppiece.py       
    Description:
        talos-puzzle pieces definition
"""

# Standards imports
from collections import namedtuple
import numpy

# Class factory
# Position is a tuple of position indexes and board
PositionIndex = namedtuple("PositionIndex", ["piece", "position"])
Position = namedtuple("Position", ["index", "board"])

# Class definition
class Piece(object):
    """Class: puzzle piece definition"""
    def __init__(self, name, label, pattern, rotations_count=1):
        """Constructor: create the piece, with its patterns"""
        # Protected members
        # Stack of piece patterns
        self.__patterns = [numpy.array(pattern)]
        for x in range(1, rotations_count):
            self.__patterns.append(numpy.rot90(numpy.array(pattern), 
            x, axes=(1, 0)))
        # Public members
        # Piece name
        self.name = name
        # Piece label
        self.label = label
        # When added to a puzzle, a piece has positions
        self.positions = [] 

    def generate_positions(self, piece_idx, board_rows, board_columns):
        """Methods: generate piece positions for the given board"""
        # Loop over all patterns
        position_idx = 0
        for pattern in self.__patterns:
            # Loop over the board cells
            pattern_rows = pattern.shape[0]
            pattern_columns = pattern.shape[1]
            rows_range = board_rows - pattern_rows + 1
            columns_range = board_columns - pattern_columns + 1
            for column in range(columns_range):
                for row in range(rows_range):
                    # Create new position
                    index = PositionIndex(piece_idx, position_idx)
                    position = Position(index, numpy.zeros((board_rows, 
                                        board_columns)))
                    # Copy the pattern in the newly created position
                    position.board[row:row + pattern_rows,
                                   column:column + pattern_columns] += pattern
                    # Add it to the position stack                      
                    self.positions.append(position)                    
                    # Move to next position
                    position_idx += 1

# Pieces definition
pieces_set = {
    "Square" : Piece("Square", "SQ", [(1, 1), (1, 1)]),
    "L right" : Piece("L right", "LR", [(1, 1), (1, 0), (1, 0)], 4),
    "L left" : Piece("L left", "LF", [(1, 1), (0, 1), (0, 1)], 4),
    "Bar" : Piece("Bar", "BA", [(1, 1, 1, 1)], 2),
    "Tee" : Piece("Tee", "TE", [(0, 1, 0), (1, 1, 1)], 4),
    "Step right" : Piece("Step right", "SR", [(0, 1, 1), (1, 1, 0)], 2),
    "Step left" : Piece("Step left", "SL", [(1, 1, 0), (0, 1, 1)], 2)
}
