#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Name: tpparam.py       
    Description:
        Parse command line to get parameters
"""

import argparse

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

# Functions
def get_parameters():
    """ Parse command line arguments """
    parser = argparse.ArgumentParser(description=DESCRIPTION_TEXT,
                                     epilog=EPILOG_TEXT,
                                     formatter_class=argparse.
                                     RawDescriptionHelpFormatter)
    group_board = parser.add_argument_group("Board", "Board dimensions")
    group_pieces = parser.add_argument_group("Pieces", "Pieces list")
    parser.add_argument("--verbose", 
        action="store_true", 
        help="Print progress status on stdout")
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
    return parser.parse_args()

def check_parameters(args):
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
            
 
