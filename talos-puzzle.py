#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Name: talos-puzzle.py
    Arguments:
        --verbose: print status on stdout
        --rows: number of board rows
        --columns: number of board columns
        --square: number of square shape pieces
        --l-right: number of L right shape pieces
        --l-left: number of L left shape pieces
        --bar: number of bar shape pieces
        --tee: number of T shape pieces
        --step-right: number of step right shape pieces
        --step-left: number of step left shape pieces
        
    Description:
        Try to solve the given puzzle and print status 
        or solution on stdout
    Requirements:
        numpy module
"""

# Standards imports
import tpparam
import tppieces
import tppuzzle

# Global varibales
__version__ = "0.0.1"
__date__ = "2018-04-28"
__author__ = "Denis Lambolez"
__contact__ = "denis.lambolez@gmail.com"
__license__ = "LGPL-3.0"

# Functions
def main():
    """ Script main function """
    # Get puzzle parameters from command line
    args = tpparam.get_parameters()

    # Create board
    puzzle = tppuzzle.Puzzle(args)

    # Add pieces, from pieces set, to the puzzle
    for _ in range(args.square):
        puzzle.add_piece(tppieces.pieces_set["Square"])
    for _ in range(args.l_right):
        puzzle.add_piece(tppieces.pieces_set["L right"])
    for _ in range(args.l_left):
        puzzle.add_piece(tppieces.pieces_set["L left"])
    for _ in range(args.bar):
        puzzle.add_piece(tppieces.pieces_set["Bar"])
    for _ in range(args.tee):
        puzzle.add_piece(tppieces.pieces_set["Tee"])
    for _ in range(args.step_right):
        puzzle.add_piece(tppieces.pieces_set["Step right"])
    for _ in range(args.step_left):
        puzzle.add_piece(tppieces.pieces_set["Step left"])

    # Solve the puzzle
    puzzle.solve()

    # Print the solutions and save the images if needed
    puzzle.solutions()
     
# Main
if __name__ == "__main__":
    main()
