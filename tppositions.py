#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Name: tppuzzle.py
    Description:
        talos-puzzle definition of positions and positions collection
"""

import numpy


class PositionsStackCollection(object):
    """Class: store a stack of positions stacks"""
    def __init__(self):
        """Constructor: create the stack"""
        self.__stack = []
        # Total combinations count
        self.__combinations_count = 1
        # Positions count per stack
        self.__positions_count = ()

    def __len__(self):
        """Method: provide 'len()' method for the collection"""
        return len(self.__stack)

    def __getitem__(self, index):
        """Method: ovverride '[]' (indexer) operator for the collection"""
        return self.__stack[index]

    @property
    def combinations_count(self):
        return self.__combinations_count

    @property
    def positions_count(self):
        return self.__positions_count

    def add(self, piece, board_rows, board_columns):
        """Method: create and add a stack of positions to the collection, for
           the given piece and board
        """
        positions_stack = PositionsStack(piece, board_rows, board_columns)
        self.__stack.append(positions_stack)
        self.__combinations_count *= len(positions_stack)
        self.__positions_count += (len(positions_stack),)

    def optimize(self):
        """Method: sort the collection of positions stacks, from smallest
           number of positions to biggest (tree crawling optimization) and then
           put the biggest at the beginning to maximize the number of crawling
           threads.
        """
        if self.__stack:
            self.__stack.sort(key=lambda stack: len(stack))
            self.__stack.insert(0, self.__stack.pop())

    def crawl_tree(self, solutions, tree_path, board, max_depth):
        """ Method: Recursive function to go through the positions
            tree and combine them to determine puzzle solutions
        """
        current_node = tree_path[-1]
        next_piece_idx = current_node[0] + 1
        # Combine current node with all nodes (positions) of next piece
        for position_idx, position in enumerate(self.__stack[next_piece_idx]):
            # Combine with next node
            next_node = (next_piece_idx, position_idx)
            # Save current board
            backup_board = numpy.copy(board)
            # Combine the positions on the board and test it
            board += position
            if numpy.max(board) <= 1:
                # We have a valid combination with next node (no overlap of
                # pieces) .Add next node to tree path
                tree_path.append(next_node)
                if current_node[0] == max_depth:
                    # We have reach the end of the tree branch, then we have a
                    # solution. Add the solution to the solutions collection
                    solutions.add(
                        self,
                        board.shape[0],
                        board.shape[1],
                        tree_path
                    )
                else:
                    # Move to the next piece
                    self.crawl_tree(solutions, tree_path, board, max_depth)
                # Restore tree path to current node
                tree_path.pop()
            # Restore board to previous state and move to next position
            board = numpy.copy(backup_board)


class PositionsStack(object):
    """Class: store a stack of positions"""
    def __init__(self, piece, board_rows, board_columns):
        """Constructor: initialize the stack of positions for the given piece
           on the given board
        """
        # Keep reference to the piece
        self.__piece = piece
        # Positions stack
        self.__stack = []
        # Loop over all piece patterns and add position to the stack
        for pattern in self.__piece.patterns:
            # Loop over the board cells
            pattern_rows = pattern.shape[0]
            pattern_columns = pattern.shape[1]
            rows_range = board_rows - pattern_rows + 1
            columns_range = board_columns - pattern_columns + 1
            for column in range(columns_range):
                for row in range(rows_range):
                    # Create new position
                    board = numpy.zeros(
                        (board_rows, board_columns),
                        numpy.uint8
                    )
                    # Copy the pattern in the newly created position
                    board[
                        row:row + pattern_rows,
                        column:column + pattern_columns
                    ] += pattern
                    # Add it to the position stack
                    self.__stack.append(board)

    def __getitem__(self, index):
        """Method: ovverride '[]' (indexer) operator for the collection"""
        return self.__stack[index]

    def __len__(self):
        """Method: provide 'len()' method for the stack"""
        return len(self.__stack)

    @property
    def piece(self):
        return self.__piece
