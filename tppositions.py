#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Name: tppuzzle.py       
    Description:
        talos-puzzle tree nodes combination
"""

import numpy

# Function
def combine_positions(pieces, solutions, tree_path, board, max_depth):
    """ Recursive function to go through the pieces / positions tree and 
        combine them to determine puzzle solutions
    """
    current_node = tree_path[-1]
    next_piece_idx = current_node[0] + 1
    # Combine current node with all nodes (positions) of next piece 
    for position_idx, position in enumerate(pieces[next_piece_idx].positions):
        # Combine with next node
        next_node = (next_piece_idx, position_idx)
        # Save current board
        backup_board = numpy.copy(board)
        # Combine the positions on the board and test it
        board += position
        if numpy.max(board) <= 1:
            # We have a valid combination with next node (no overlap of pieces)
            # Add next node to tree path
            tree_path.append(next_node)
            if current_node[0] == max_depth:
                # We have reach the end of the tree branch, then we have a
                # solution. Add the solution to the solutions collection
                solutions.add(pieces, board.shape[0], board.shape[1],
                              tree_path)
            else:
                # Move to the next piece
                combine_positions(pieces, solutions, tree_path, board, 
                                  max_depth)
            # Restore tree path to current node
            tree_path.pop()
        # Restore board to previous state and move to next position
        board = numpy.copy(backup_board)
