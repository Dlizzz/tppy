#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Name: tppiece.py
    Description:
        talos-puzzle pieces definition
"""

import numpy


class PiecesCollection(object):
    """Class: define a collection of pieces"""

    def __init__(self):
        """Constructor: initialize the pieces stack"""
        self.__stack = []

    def __len__(self):
        """Method: ovverride 'len()' method for the collection"""
        return len(self.__stack)

    def __getitem__(self, index):
        """Method: ovverride '[]' (indexer) operator for the collection"""
        return self.__stack[index]

    def append(self, piece):
        """Method: add a piece to the collection"""
        self.__stack.append(piece)


class Piece(object):
    """Class: puzzle piece definition"""

    def __init__(self, name, label, pattern, rotations_count=1):
        """Constructor: create the piece, with its patterns"""
        # Protected members
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
        return self.__name

    @property
    def label(self):
        return self.__label

    @property
    def patterns(self):
        return self.__patterns


# Pieces definition
pieces_set = {
    "Square": Piece("Square", "SQ", [(1, 1), (1, 1)]),
    "L right": Piece("L right", "LR", [(1, 1), (1, 0), (1, 0)], 4),
    "L left": Piece("L left", "LL", [(1, 1), (0, 1), (0, 1)], 4),
    "Bar": Piece("Bar", "BA", [(1, 1, 1, 1)], 2),
    "Tee": Piece("Tee", "TE", [(0, 1, 0), (1, 1, 1)], 4),
    "Step right": Piece("Step right", "SR", [(0, 1, 1), (1, 1, 0)], 2),
    "Step left": Piece("Step left", "SL", [(1, 1, 0), (0, 1, 1)], 2)
}
