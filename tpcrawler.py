#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Name: tpcrawler.py
    Description:
        talos-puzzle tree crawler sub-process definition
"""

import numpy


def crawler(positions, tree_path, board, max_depth, queue, found):
    """
    Function: Recursive function to go through the positions
    tree and combine them to determine puzzle solutions.
    Function is designed to be run in a subprocess.
    """
    current_node = tree_path[-1]
    next_piece_idx = current_node[0] + 1
    # Combine current node with all nodes (positions) of next piece
    for position_idx, position in enumerate(positions[next_piece_idx]):
        # If main process indicates that solution is found, exits immediately
        if found.is_set():
            break
        # Next node
        next_node = (next_piece_idx, position_idx)
        # Save current board
        backup_board = numpy.copy(board)
        # Combine the positions on the board and test it
        board += position
        if numpy.max(board) <= 1:
            # We have a valid combination with next node (no overlap of
            # pieces). Add next node to tree path
            tree_path.append(next_node)
            if current_node[0] == max_depth:
                # We have reach the end of the tree branch, then we have a
                # solution. Send valid tree path to main process.
                queue.put(tree_path)
            else:
                # Move to the next piece
                crawler(positions, tree_path, board, max_depth, queue, found)
            # Restore tree path to current node
            tree_path.pop()
        # Restore board to previous state and move to next position
        board = numpy.copy(backup_board)
