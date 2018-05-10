#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Name: tpparam.py       
    Description:
        Parse command line to get parameters
"""

import argparse
import os
from PIL import ImageColor

# Help text
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
The pieces can be flipped horizontally and vertically."""

# Class
class writeable_dir(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if not os.path.isdir(values):
            raise argparse.ArgumentTypeError("writeable_dir:{0} is not a " 
                                             "valid path".format(values))
        if os.access(values, os.W_OK):
            setattr(namespace,self.dest,values)
        else:
            raise argparse.ArgumentTypeError("writeable_dir:{0} is not a "  
                                             "writeable dir".format(values))

# Functions
def get_parameters():
    """ Parse command line arguments """
    # Create parser and define parameters
    parser = argparse.ArgumentParser(description=DESCRIPTION_TEXT,
                                     epilog=EPILOG_TEXT,
                                     formatter_class=argparse.
                                     RawDescriptionHelpFormatter)
    group_board = parser.add_argument_group("Board", "Board dimensions")
    group_pieces = parser.add_argument_group("Pieces", "Pieces list")
    group_solutions = parser.add_argument_group("Solutions", 
                                                "Solutions output")
    parser.add_argument("--verbose", 
        action="store_true", 
        help="Print progress status on stdout")
    parser.add_argument("--first", 
        action="store_true", 
        help="Stop at first solution found")
    group_board.add_argument("--rows",
        help="Number of board rows",
        type=int,
        required=True)
    group_board.add_argument("--columns",
        help="Number of board columns",
        type=int,
        required=True)
    group_pieces.add_argument("--square",
        type=int,
        default=0,
        help="Number of Square shape pieces")
    group_pieces.add_argument("--l-right",
        type=int,
        default=0,
        help="Number of L right shape pieces")
    group_pieces.add_argument("--l-left",
        type=int,
        default=0,
        help="Number of L left shape pieces")
    group_pieces.add_argument("--bar",
        type=int,
        default=0,
        help="Number of Bar shape pieces")
    group_pieces.add_argument("--tee",
        type=int,
        default=0,
        help="Number of T shape pieces")
    group_pieces.add_argument("--step-right",
        type=int,
        default=0,
        help="Number of Step right shape pieces")
    group_pieces.add_argument("--step-left",
        type=int,
        default=0,
        help="Number of Step left shape pieces")
    group_solutions.add_argument("--images",
        action="store_true", 
        help="Output solutions as png images")
    group_solutions.add_argument("--output-dir",
        action=writeable_dir,
        default=os.getcwd(), 
        help="Directory where to output png images")
    group_solutions.add_argument("--cell-size",
        type=int,
        default=100,
        help="Size in pixels of one cell of the board")
    group_solutions.add_argument("--shape-color",
        default="Yellow",
        help="Color name (HTML) of the shape color")
    group_solutions.add_argument("--fill-color",
        default="DarkMagenta",
        help="Color name (HTML) of the fill color")

    # Get parameters
    args = parser.parse_args()

    # Check_parameters
    if args.rows < 1:
        print("Fatal: Rows number must be > 0 !")
        exit(1)
    if args.columns < 1:
        print("Fatal: Columns number must be > 0 !")
        exit(1)
    if args.square < 0:
        print("Fatal: Square number must be >= 0 !")
        exit(1)
    if args.l_right < 0:
        print("Fatal: L right number must be >= 0 !")
        exit(1)
    if args.l_left < 0:
        print("Fatal: L left number must be >= 0 !")
        exit(1)
    if args.bar < 0:
        print("Fatal: Bar number must be >= 0 !")
        exit(1)
    if args.tee < 0:
        print("Fatal: Tee number must be >= 0 !")
        exit(1)
    if args.step_right < 0:
        print("Fatal: Step right number must be >= 0 !")
        exit(1)
    if args.step_left < 0:
        print("Fatal: Step left number must be >= 0 !")
        exit(1)
    if (args.rows * args.columns) != ((args.square + args.l_right 
        + args.l_left + args.bar + args.tee + args.step_right
        + args.step_left) * 4):
        print("Fatal: Board size (rows x columns) must equal sum of" 
              + " pieces size (4)")
        exit(1)
    if args.cell_size < 1:
        print("Info: Cell size must be > 0 ! Using default size.")
        args.cell_size = 100
    try:
        ImageColor.getrgb(args.shape_color)
    except:
        print("Info: Wrong color name for shape! Using default color.")
        args.shape_color = "Yellow"
    try:
        ImageColor.getrgb(args.fill_color)
    except:
        print("Info: Wrong color name for fill! Using default color.")
        args.fill_color = "DarkMagenta"

    return args


    
            
 
