#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Module: Entry point of talospuzzle application

Name: talospuzzle.py
Comments:
    Puzzle board is made of Rows x Columns cells.
    Column is the horizontal dimension. Row is the vertical dimension.
    The puzzle can use the following pieces:
    - Square shape:
        XX
        XX
    - L right shape:
        XX
        X
        X
    - L left shape:
        XX
        X
        X
    - Bar shape:
        X
        X
        X
        X
    - Tee shape:
        X
        XXX
    - Step right shape:
        XX
        XX
    - Step left shape:
        XX
        XX
    The pieces can be flipped horizontally and vertically.
Command line arguments:
    --verbose: Print progress status on stdout (toggle, default: false)
    --first: Stop at first solution found (toggle, default: false)
    --stats: Save puzzle solving statistics in CSV format
        (toggle, default: false)
    --rows #: Number of board rows (mandatory, no default)
    --columns #: Number of board columns (mandatory, no default)
    --square #: Number of Square shape pieces (default: 0)
    --l-right #: Number of L right shape pieces (default: 0)
    --l-left #: Number of L left shape pieces (default: 0)
    --bar #: Number of Bar shape pieces (default: 0)
    --tee #: Number of T shape pieces (default: 0)
    --step-right #: Number of Step right shape pieces (default: 0)
    --step-left #: Number of Step left shape pieces (default: 0)
    --images: Output solutions as png images (toggle, default: false)
    --output-dir dir: Directory where to output png images
        (default: application dir)
    --cell-size #: Size in pixels of one cell of the board (default: 100)
    --shape-color colorname: Color name (HTML) of the shape color
        (default: "Yellow")
    --fill-color colorname: Color name (HTML) of the fill color
        (default: "DatkMagenta")
Functions:
    main: application main function
Attributes:
    __version__: string
    __date__: string
    __author__: string
    __contact__: string
    __license__: string
Dependencies:
    multiprocessing
    tpparam
    tppieces
    tppuzzle
"""

import multiprocessing as mp

from tpparam import get_parameters
from tppieces import pieces_set
from tppuzzle import Puzzle
from tperrors import TalosArgumentError, TalosFileSystemError

__version__ = "2.1.0"
__date__ = "2018-05-21"
__author__ = "Denis Lambolez"
__contact__ = "denis.lambolez@gmail.com"
__license__ = "LGPL-3.0"


def main():
    """Function: Create puzzle, add pieces, solve and display solutions"""

    # Get puzzle parameters from command line
    try:
        args = get_parameters()
    except TalosArgumentError as err:
        print("Argument error: {} - {}".format(err.argument, err.message))
        exit(1)

    # Create board
    puzzle = Puzzle(args)

    # Add pieces, from pieces set, to the puzzle
    for _ in range(args.square):
        puzzle.add_piece(pieces_set["Square"])
    for _ in range(args.l_right):
        puzzle.add_piece(pieces_set["L Right"])
    for _ in range(args.l_left):
        puzzle.add_piece(pieces_set["L Left"])
    for _ in range(args.bar):
        puzzle.add_piece(pieces_set["Bar"])
    for _ in range(args.tee):
        puzzle.add_piece(pieces_set["Tee"])
    for _ in range(args.step_right):
        puzzle.add_piece(pieces_set["Step Right"])
    for _ in range(args.step_left):
        puzzle.add_piece(pieces_set["Step Left"])

    # Solve the puzzle
    try:
        puzzle.solve()
    except TalosFileSystemError as err:
        print(err.message, " with system error: ", err.syserror)

    # Print the solutions and save the images if needed
    try:
        puzzle.solutions()
    except TalosFileSystemError as err:
        print(err.message, " with system error: ", err.syserror)


# Application entry point
if __name__ == "__main__":
    # Make sure that we use 'spawn' method for subprocesses
    mp.set_start_method("spawn")
    main()
