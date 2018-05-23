#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Define PositionsStack and PositionsStackCollection

Name: tppositions.py
Classes:
    PositionsStackCollection: collection of PositionsStack - all posibble
        positions of puzzle pieces on the board
    PositionsStack: all possible positions of one piece on the board
Dependencies:
    numpy
"""

import numpy


class PositionsStackCollection(object):
    """Define a collection of pieces positions to solve the puzzle

    Public members:
        Properties:
            combinations_count: integer - total number of combinations
        Methods:
            add: create and append a positions stack to the collection
            optimize: optimize the tree crawling by ordering the collection
                from the smallest number of positions to the biggest
    Private members:
        Attributes:
            __stack: list of PositionsStack - store the positions for pieces
            __combinations_count: integer - total number of combinations
    Special methods:
        __init__: override object constructor
        __len__: provide len method, # of items in the collection
        __getitem__: provide indexer ([]) operator, collection is iterable
    """

    def __init__(self):
        """Create the PositionsStack stack"""

        self.__stack = []
        # Total combinations count
        self.__combinations_count = 1

    def __len__(self):
        """Provide len method, # of items in the collection

        Return: integer - # of items in the collection
        """

        return len(self.__stack)

    def __getitem__(self, index):
        """Provide indexer ([]) operator, collection is iterable

        Inputs:
            index: integer - index of the requested item
        Return: list of numpy arrays - a piece positions
        """

        return self.__stack[index]

    @property
    def combinations_count(self):
        """integer - total count of combinations"""

        return self.__combinations_count

    def add(self, piece, board_rows, board_columns):
        """Create and add a stack of positions to the collection, for
        the given piece and board

        Inputs:
            piece: Piece - the piece of which we add the positions
            board_rows: integer - number of rows on the board
            board_columns: integer - number of columns on the board
        """

        positions_stack = PositionsStack(piece, board_rows, board_columns)
        self.__stack.append(positions_stack)
        self.__combinations_count *= len(positions_stack)

    def optimize(self):
        """Sort the collection of positions stacks, from smallest
        number of positions to biggest
        """

        if self.__stack:
            self.__stack.sort(key=lambda stack: len(stack))
            # self.__stack.insert(0, self.__stack.pop())


class PositionsStack(object):
    """Store a stack of positions for one piece

    Public members:
        Properties:
            piece: Piece - the piece of which we have the positions
    Private members:
        Attributes:
            __stack: list of numpy arrays - store the positions for the piece
            __piece: Piece - the piece of which we have the positions
    Special methods:
        __init__: override object constructor
        __len__: provide len method, # of items in the list
        __getitem__: provide indexer ([]) operator, list is iterable
    """

    def __init__(self, piece, board_rows, board_columns):
        """Initialize the stack of positions for the given piece on the given
        board

        Inputs:
            piece: Piece - the piece of which we store the positions
            board_rows: integer - number of rows on the board
            board_columns: integer - number of columns on the board
        """

        # Keep reference to the piece
        self.__piece = piece
        # Positions stack
        self.__stack = []
        # Loop over all piece patterns and add position to the stack
        for pattern in self.__piece.patterns:
            # Loop over the board cells
            pattern_rows = pattern.shape[0]
            pattern_columns = pattern.shape[1]
            rows_range = board_rows - pattern_rows + 1
            columns_range = board_columns - pattern_columns + 1
            for column in range(columns_range):
                for row in range(rows_range):
                    # Create new position
                    board = numpy.zeros(
                        (board_rows, board_columns),
                        numpy.uint8
                    )
                    # Copy the pattern in the newly created position
                    board[
                        row:row + pattern_rows,
                        column:column + pattern_columns
                    ] += pattern
                    # Add it to the position stack
                    self.__stack.append(board)

    def __getitem__(self, index):
        """Ovverride '[]' (indexer) operator for the collection

        Inputs:
            index: integer - index of the requested item
        Return: numpy array - position of a piece
        """

        return self.__stack[index]

    def __len__(self):
        """Provide 'len()' method for the stack

        Return: integer - # of items in the list
        """

        return len(self.__stack)

    @property
    def piece(self):
        """Piece - the piece of which we store the positions"""

        return self.__piece
