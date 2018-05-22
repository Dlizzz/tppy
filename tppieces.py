#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Module: Define Piece and PiecesCollection

Name: tppieces.py
Classes:
    PiecesCollection: collection of Piece - pieces set to solve the puzzle
    Piece: piece description
Attributes:
    pieces_set: static dict of Piece - description of all pieces
Dependencies:
    numpy
"""

import numpy


class PiecesCollection(object):
    """Class: define a collection of pieces to solve the puzzle

    Public members:
        Methods:
            append: append a existing piece to the collection
    Private members:
        Methods:
            __supervise: watch all crawler processes for termination
    Special methods:
        __init__: override object constructor
        __len__: provide len method, # of items in the collection
        __getitem__: provide indexer ([]) operator, collection is iterable
    """

    def __init__(self):
        """Constructor: initialize the pieces stack"""

        self.__stack = []

    def __len__(self):
        """Method: provide len method, # of items in the collection"""

        return len(self.__stack)

    def __getitem__(self, index):
        """Method: provide [] operator, collection is iterable"""

        return self.__stack[index]

    def append(self, piece):
        """Method: append given piece to the collection"""

        self.__stack.append(piece)


class Piece(object):
    """Class: define a piece

    Public members:
        Methods:
            name: property, string - name of the piece
            label: property, string - label of the piece
            patterns: property, list of numpy arrays - patterns of the piece
    Private members:
        Attributes:
            __name: string - name of the piece
            __label: string - label of the piece
            __patterns: list of numpy arrays - patterns of the piece
    Special methods:
        __init__: override object constructor
    """

    def __init__(self, name, label, pattern, rotations_count=1):
        """Constructor: create the piece, with its patterns

        Inputs:
            name: string - name of the piece
            label: string - label of the piece
            pattern: list of tuples - initial pattern of the piece 
            rotations_count: integer - # of 90° rotations to do to obtain all
                the patterns of the piece
        """
        # Stack of piece patterns
        self.__patterns = [numpy.array(pattern, numpy.uint8)]
        for x in range(1, rotations_count):
            self.__patterns.append(
                numpy.rot90(
                    numpy.array(
                        pattern,
                        numpy.uint8
                    ),
                    x,
                    axes=(1, 0)
                )
            )
        # Piece name
        self.__name = name
        # Piece label
        self.__label = label

    @property
    def name(self):
        """Property: string - name of piece"""

        return self.__name

    @property
    def label(self):
        """Property: string - label of piece"""

        return self.__label

    @property
    def patterns(self):
        """Property: list of numpy arrays - patterns of piece"""

        return self.__patterns


# Pieces definition
pieces_set = {
    "Square": Piece("Square", "SQ", [(1, 1), (1, 1)]),
    "L Right": Piece("L Right", "LR", [(1, 1), (1, 0), (1, 0)], 4),
    "L Left": Piece("L Left", "LL", [(1, 1), (0, 1), (0, 1)], 4),
    "Bar": Piece("Bar", "BA", [(1, 1, 1, 1)], 2),
    "Tee": Piece("Tee", "TE", [(0, 1, 0), (1, 1, 1)], 4),
    "Step Right": Piece("Step Right", "SR", [(0, 1, 1), (1, 1, 0)], 2),
    "Step Left": Piece("Step Left", "SL", [(1, 1, 0), (0, 1, 1)], 2)
}
