#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Module: Parse, check and return command line arguments

Name: tpparam.py
Classes:
    WriteableDir: argparse.Action - check that directory is writeable
    StrictlyPositive: argparse.Action - check that value is strictly positive
    Positive: argparse.Action - check that value is positive or null
    ValidColorName: argparse.Action - check that value is a HTML color name
Functions:
    get_parameters: argparse.args - return validated command line arguments
Attributes:
    DESCRIPTION_TEXT: const string - description text for help
    EPILOG_TEXT: : const string - epilog text for help
Dependencies:
    argparse
    os
    PIL
    tperrors
"""

import argparse
import os

from PIL import ImageColor

from tperrors import TalosError


DESCRIPTION_TEXT = """Try to solve the given puzzle and print status
or solution if it exists on stdout."""
EPILOG_TEXT = """Puzzle board is made of Rows x Columns cells.
Column is the horizontal dimension.
Row is the vertical dimension.
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
"""


class WriteableDir(argparse.Action):
    """Class: argparse action to check that a given directory is writeable

    Inherit:
        argparse.Actions
    Special methods:
        __call__: override argparse.Action __call__
    Exceptions:
        argparse.ArgumentError: path not valid or not writeable
    """

    def __call__(self, parser, namespace, values, option_string=None):
        """Method: test if directory is valid and writeable, raise error if not

        Inputs:
            parser: ArgumentParser - object which contains this action.
            values: string - The associated command-line arguments, with any
                type conversions applied.
            option_string: string, optional, None - The option string that was
                used to invoke this action.
        Outputs:
            namespace: Namespace - object that will be returned by parse_args()
        Exceptions:
            argparse.ArgumentError: path not valid or not writeable
        """

        if not os.path.isdir(values):
            raise argparse.ArgumentError(
                super().argument,
                "{} is not a valid path"
                .format(values)
            )
        if not os.access(values, os.W_OK):
            raise argparse.ArgumentError(
                super().argument,
                "{} is not a writeable dir"
                .format(values)
            )
        setattr(namespace, self.dest, values)


class ValidColorName(argparse.Action):
    """Class: argparse action to check that a value is a valid HTML color name

    Inherit:
        argparse.Actions
    Special methods:
        __call__: override argparse.Action __call__
    Exceptions:
        argparse.ArgumentError: value is not a valid HTML color name
    """

    def __call__(self, parser, namespace, values, option_string=None):
        """Method: test if value is a valid color name, raise error if not

        Inputs:
            parser: ArgumentParser - object which contains this action.
            values: int - The associated command-line arguments, with any
                type conversions applied.
            option_string: string, optional, None - The option string that was
                used to invoke this action.
        Outputs:
            namespace: Namespace - object that will be returned by parse_args()
        Exceptions:
            argparse.ArgumentError: value not strictly positive
        """

        try:
            ImageColor.getrgb(values)
        except ValueError:
            raise argparse.ArgumentError(
                super().argument,
                "Not a valid HTML color name !"
            )
        setattr(namespace, self.dest, values)


class StrictlyPositive(argparse.Action):
    """Class: argparse action to check that a value is strictly positive

    Inherit:
        argparse.Actions
    Special methods:
        __call__: override argparse.Action __call__
    Exceptions:
        argparse.ArgumentError: value is not strictly positive
    """

    def __call__(self, parser, namespace, values, option_string=None):
        """Method: test if value is strictly positive, raise error if not

        Inputs:
            parser: ArgumentParser - object which contains this action.
            values: int - The associated command-line arguments, with any
                type conversions applied.
            option_string: string, optional, None - The option string that was
                used to invoke this action.
        Outputs:
            namespace: Namespace - object that will be returned by parse_args()
        Exceptions:
            argparse.ArgumentError: value not strictly positive
        """

        if not values > 0:
            raise argparse.ArgumentError(
                super().argument,
                "Value is not strictly positive"
            )
        setattr(namespace, self.dest, values)


class Positive(argparse.Action):
    """Class: argparse action to check that a value is positive (null included)

    Inherit:
        argparse.Actions
    Special methods:
        __call__: override argparse.Action __call__
    Exceptions:
        argparse.ArgumentError: value is not positive or null
    """

    def __call__(self, parser, namespace, values, option_string=None):
        """Method: test if value is positive or null, raise error if not

        Inputs:
            parser: ArgumentParser - object which contains this action.
            values: int - The associated command-line arguments, with any
                type conversions applied.
            option_string: string, optional, None - The option string that was
                used to invoke this action.
        Outputs:
            namespace: Namespace - object that will be returned by parse_args()
        Exceptions:
            argparse.ArgumentError: value not strictly positive
        """

        if not values >= 0:
            raise argparse.ArgumentError(
                super().argument,
                "Value is not positive or null"
            )
        setattr(namespace, self.dest, values)


def get_parameters():
    """Function: Parse, check and return command line arguments

    Return:
        args: argparse.args - the validated arguments
    Exceptions:
        argparse.ArgumentError: invalid argument
    """
    # Create parser and define parameters
    parser = argparse.ArgumentParser(description=DESCRIPTION_TEXT,
                                     epilog=EPILOG_TEXT,
                                     formatter_class=argparse.
                                     RawDescriptionHelpFormatter)
    group_board = parser.add_argument_group("Board", "Board dimensions")
    group_pieces = parser.add_argument_group("Pieces", "Pieces list")
    group_solutions = parser.add_argument_group("Solutions",
                                                "Solutions output")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print progress status on stdout"
    )
    parser.add_argument(
        "--first",
        action="store_true",
        help="Stop at first solution found"
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Save puzzle solving statistics in CSV format"
    )
    group_board.add_argument(
        "--rows",
        action=StrictlyPositive,
        help="Number of board rows",
        type=int,
        required=True
    )
    group_board.add_argument(
        "--columns",
        action=StrictlyPositive,
        help="Number of board columns",
        type=int,
        required=True
    )
    group_pieces.add_argument(
        "--square",
        action=Positive,
        type=int,
        default=0,
        help="Number of Square shape pieces"
    )
    group_pieces.add_argument(
        "--l-right",
        action=Positive,
        type=int,
        default=0,
        help="Number of L right shape pieces"
    )
    group_pieces.add_argument(
        "--l-left",
        action=Positive,
        type=int,
        default=0,
        help="Number of L left shape pieces"
    )
    group_pieces.add_argument(
        "--bar",
        action=Positive,
        type=int,
        default=0,
        help="Number of Bar shape pieces"
    )
    group_pieces.add_argument(
        "--tee",
        action=Positive,
        type=int,
        default=0,
        help="Number of T shape pieces"
    )
    group_pieces.add_argument(
        "--step-right",
        action=Positive,
        type=int,
        default=0,
        help="Number of Step right shape pieces"
    )
    group_pieces.add_argument(
        "--step-left",
        action=Positive,
        type=int,
        default=0,
        help="Number of Step left shape pieces"
    )
    group_solutions.add_argument(
        "--images",
        action="store_true",
        help="Output solutions as png images"
    )
    group_solutions.add_argument(
        "--output-dir",
        action=WriteableDir,
        default=os.getcwd(),
        help="Directory where to output png images"
    )
    group_solutions.add_argument(
        "--cell-size",
        action=StrictlyPositive,
        type=int,
        default=100,
        help="Size in pixels of one cell of the board"
    )
    group_solutions.add_argument(
        "--shape-color",
        action=ValidColorName,
        default="Yellow",
        help="Color name (HTML) of the shape color"
    )
    group_solutions.add_argument(
        "--fill-color",
        action=ValidColorName,
        default="DarkMagenta",
        help="Color name (HTML) of the fill color"
    )

    # Get parameters
    args = parser.parse_args()

    # Check_parameters
    if (args.rows * args.columns) != (
        (
            args.square
            + args.l_right
            + args.l_left
            + args.bar
            + args.tee
            + args.step_right
            + args.step_left
        ) * 4
    ):
        raise TalosError("Board size must equal sum of pieces size (4)")

    return args
