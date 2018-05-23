#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Parse, check and return command line arguments

Name: tpparam.py
Classes:
    WriteableDir: argparse.Action - check that directory is writeable
    StrictlyPositive: argparse.Action - check that value is strictly positive
    Positive: argparse.Action - check that value is positive or null
    ValidColorName: argparse.Action - check that value is a HTML color name
    TalosArguments: argparse.ArgumentParser - all command line arguments
Attributes:
    DESCRIPTION_TEXT: const string - description text for help
    EPILOG_TEXT: : const string - epilog text for help
Dependencies:
    argparse
    os
    PIL
    tperrors
"""

import os
from argparse import Action, ArgumentParser, RawDescriptionHelpFormatter

from PIL import ImageColor

from tperrors import TalosArgumentError


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


class WriteableDir(Action):
    """Argparse action to check that a given directory is writeable

    Inherit:
        argparse.Actions
    Special methods:
        __call__: override argparse.Action __call__
    Exceptions:
        TalosArgumentError: path not valid or not writeable
    """

    def __call__(self, parser, namespace, values, option_string=None):
        """Test if directory is valid and writeable, raise error if not

        Inputs:
            parser: ArgumentParser - object which contains this action.
            values: string - The associated command-line arguments, with any
                type conversions applied.
            option_string: string, optional, None - The option string that was
                used to invoke this action.
        Outputs:
            namespace: Namespace - object that will be returned by parse_args()
        Exceptions:
            TalosArgumentError: path not valid or not writeable
        """

        if not os.path.isdir(values):
            raise TalosArgumentError(
                "{} is not a valid path"
                .format(values),
                option_string
            )
        if not os.access(values, os.W_OK):
            raise TalosArgumentError(
                "{} is not a writeable dir"
                .format(values),
                option_string
            )
        setattr(namespace, self.dest, values)


class ValidColorName(Action):
    """Argparse action to check that a value is a valid HTML color name

    Inherit:
        argparse.Actions
    Special methods:
        __call__: override argparse.Action __call__
    Exceptions:
        TalosArgumentError: value is not a valid HTML color name
    """

    def __call__(self, parser, namespace, values, option_string=None):
        """Test if value is a valid color name, raise error if not

        Inputs:
            parser: ArgumentParser - object which contains this action.
            values: int - The associated command-line arguments, with any
                type conversions applied.
            option_string: string, optional, None - The option string that was
                used to invoke this action.
        Outputs:
            namespace: Namespace - object that will be returned by parse_args()
        Exceptions:
            TalosArgumentError: value not strictly positive
        """

        try:
            ImageColor.getrgb(values)
        except ValueError:
            raise TalosArgumentError(
                "Not a valid HTML color name !",
                option_string
            )
        setattr(namespace, self.dest, values)


class StrictlyPositive(Action):
    """Argparse action to check that a value is strictly positive

    Inherit:
        argparse.Actions
    Special methods:
        __call__: override argparse.Action __call__
    Exceptions:
        TalosArgumentError: value is not strictly positive
    """

    def __call__(self, parser, namespace, values, option_string=None):
        """Test if value is strictly positive, raise error if not

        Inputs:
            parser: ArgumentParser - object which contains this action.
            values: int - The associated command-line arguments, with any
                type conversions applied.
            option_string: string, optional, None - The option string that was
                used to invoke this action.
        Outputs:
            namespace: Namespace - object that will be returned by parse_args()
        Exceptions:
            TalosArgumentError: value not strictly positive
        """

        if not values > 0:
            raise TalosArgumentError(
                "Value is not strictly positive",
                option_string
            )
        setattr(namespace, self.dest, values)


class Positive(Action):
    """Argparse action to check that a value is positive (null included)

    Inherit:
        argparse.Actions
    Special methods:
        __call__: override argparse.Action __call__
    Exceptions:
        TalosArgumentError: value is not positive or null
    """

    def __call__(self, parser, namespace, values, option_string=None):
        """Test if value is positive or null, raise error if not

        Inputs:
            parser: ArgumentParser - object which contains this action.
            values: int - The associated command-line arguments, with any
                type conversions applied.
            option_string: string, optional, None - The option string that was
                used to invoke this action.
        Outputs:
            namespace: Namespace - object that will be returned by parse_args()
        Exceptions:
            TalosArgumentError: value not strictly positive
        """

        if not values >= 0:
            raise TalosArgumentError(
                "Value is not positive or null",
                option_string
            )
        setattr(namespace, self.dest, values)


class TalosArguments(ArgumentParser):
    """Parse the command line, check and provide the arguments

    Inherit:
        argparse.ArgumentParser
    Private members:
        Attributes:
            __group_board: argparse.ArgumentGroup - board parameters
            __group_pieces: argparse.ArgumentGroup - pieces parameters
            __group_solutions:argparse.ArgumentGroup - solutions parameters
    Special methods:
        __init__: extend ArgumentParser constructor
        __call__: return the args attributes of ArgumentParser
    Exceptions:
        TalosArgumentError: error in argument parsing
    """

    def __init__(self):
        """Extend ArgumentParser constructor. Parse and check command line
        arguments

        Exceptions:
            TalosArgumentError: invalid argument
        """
        # Init parser from super class
        super().__init__(
            description=DESCRIPTION_TEXT,
            epilog=EPILOG_TEXT,
            formatter_class=RawDescriptionHelpFormatter
        )
        self.__group_board = super().add_argument_group(
            "Board",
            "Board dimensions"
        )
        self.__group_pieces = super().add_argument_group(
            "Pieces",
            "Pieces list"
        )
        self.__group_solutions = super().add_argument_group(
            "Solutions",
            "Solutions output"
        )
        super().add_argument(
            "--verbose",
            action="store_true",
            help="Print progress status on stdout"
        )
        super().add_argument(
            "--first",
            action="store_true",
            help="Stop at first solution found"
        )
        super().add_argument(
            "--stats",
            action="store_true",
            help="Save puzzle solving statistics in CSV format"
        )
        self.__group_board.add_argument(
            "--rows",
            action=StrictlyPositive,
            help="Number of board rows",
            type=int,
            required=True
        )
        self.__group_board.add_argument(
            "--columns",
            action=StrictlyPositive,
            help="Number of board columns",
            type=int,
            required=True
        )
        self.__group_pieces.add_argument(
            "--square",
            action=Positive,
            type=int,
            default=0,
            help="Number of Square shape pieces"
        )
        self.__group_pieces.add_argument(
            "--l-right",
            action=Positive,
            type=int,
            default=0,
            help="Number of L right shape pieces"
        )
        self.__group_pieces.add_argument(
            "--l-left",
            action=Positive,
            type=int,
            default=0,
            help="Number of L left shape pieces"
        )
        self.__group_pieces.add_argument(
            "--bar",
            action=Positive,
            type=int,
            default=0,
            help="Number of Bar shape pieces"
        )
        self.__group_pieces.add_argument(
            "--tee",
            action=Positive,
            type=int,
            default=0,
            help="Number of T shape pieces"
        )
        self.__group_pieces.add_argument(
            "--step-right",
            action=Positive,
            type=int,
            default=0,
            help="Number of Step right shape pieces"
        )
        self.__group_pieces.add_argument(
            "--step-left",
            action=Positive,
            type=int,
            default=0,
            help="Number of Step left shape pieces"
        )
        self.__group_solutions.add_argument(
            "--images",
            action="store_true",
            help="Output solutions as png images"
        )
        self.__group_solutions.add_argument(
            "--output-dir",
            action=WriteableDir,
            default=os.getcwd(),
            help="Directory where to output png images"
        )
        self.__group_solutions.add_argument(
            "--cell-size",
            action=StrictlyPositive,
            type=int,
            default=100,
            help="Size in pixels of one cell of the board"
        )
        self.__group_solutions.add_argument(
            "--shape-color",
            action=ValidColorName,
            default="Yellow",
            help="Color name (HTML) of the shape color"
        )
        self.__group_solutions.add_argument(
            "--fill-color",
            action=ValidColorName,
            default="DarkMagenta",
            help="Color name (HTML) of the fill color"
        )

        # Get parameters
        self.__args = super().parse_args()

        # Check_parameters
        if (self.__args.rows * self.__args.columns) != (
            (
                self.__args.square
                + self.__args.l_right
                + self.__args.l_left
                + self.__args.bar
                + self.__args.tee
                + self.__args.step_right
                + self.__args.step_left
            ) * 4
        ):
            raise TalosArgumentError(
                "Board size must equal sum of pieces size (4)",
                "--rows x --columns"
            )

    def __call__(self):
        """Class is callable. Return the args component

        Return: argparse.args
        """

        return self.__args
