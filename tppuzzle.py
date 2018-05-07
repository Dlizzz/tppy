#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Name: tppuzzle.py       
    Description:
        talos-puzzle puzzle definition
"""
import os
import sys
import numpy
import time
import copy
import tppieces
import tpimages
from PIL import ImageColor
from collections import namedtuple

# Class definition
class Puzzle(object):
    """Class: game board and stack of solutions"""
    def __init__(self, args):
        """Constructor: create board with rows x columns dimension"""
        # Protected members
        # Do we have to be verbose
        self.__verbose = args.verbose
        # Do we stop at first solution found
        self.__first = args.first
        # Images output
        self.__images = args.images      
        self.__cell_size = args.cell_size
        self.__fill_color = ImageColor.getrgb(args.fill_color)
        self.__shape_color = ImageColor.getrgb(args.shape_color)
        self.__output_dir = (args.output_dir + "\\Board {}R x {}C - {}LR {}LL "
                             "{}TE {}BA {}SQ {}SR {}SL".format(args.rows, 
                             args.columns, args.l_right, args.l_left, args.tee,
                             args.bar, args.square, args.step_right, 
                             args.step_left))
        # Game board dimensions and board
        self.__board_rows = args.rows
        self.__board_columns = args.columns
        self.__board = numpy.zeros((args.rows, args.columns), numpy.uint8)
        # Stack of pieces with positions
        self.__pieces = []
        # Tree path, stack of tuples(piece_idx, position_idx)
        self.__tree_path = []
        # Solution nodes, stack of stack of valid tree path
        self.__solutions_nodes = [] 
        # Solutions with label to remove duplicates
        self.__solutions_label = []
        # Solutions with pieces index to draw solution
        self.__solutions_pieces = []
        # Total combinations count
        self.__combinations_count = 1
        if self.__verbose:
            print("Info: Create puzzle with {} rows and {} columns."
                  .format(self.__board_rows, self.__board_columns))
            print("Info: Board size is {}.".format(self.__board_rows
                                                   * self.__board_columns))
            if self.__images:
                print("Info: Solutions image will be generated in {} "
                      "with a cell size of {}."
                      .format(self.__output_dir, self.__cell_size))
  
    def __tree_path_backward(self):
        """Method (protected): go backward on the tree path, until we find 
           a node with a possible next position, then recreate the board at 
           this node. Return false if we can't find a next position anymore"""
        while True:
            # Next position for current node
            piece_idx = self.__tree_path[-1][0]
            position_idx = self.__tree_path[-1][1] + 1
            # Move to previous node, if it exists
            self.__tree_path.pop()
            if self.__tree_path == []:
                # No more node, can't go backward
                backward_status = False
                break
            # If we have a next position
            if position_idx < len(self.__pieces[piece_idx].positions):
                # Recreate the board at the new node and return ok
                self.__board = numpy.zeros((self.__board_rows, 
                                           self.__board_columns),
                                           numpy.uint8)
                for node in self.__tree_path:
                    self.__board += self.__pieces[node[0]].positions[node[1]]
                backward_status = True
                break
            # Else continue backward in tree path 
        return (backward_status, piece_idx, position_idx)

    def __print_tree_path(self):
        """Method (protected): format and print the tree path"""
        tree_path = ""
        for piece_idx in range(len(self.__pieces)):
            if piece_idx < len(self.__tree_path):
                # Insert the position number of the corresponding piece
                tree_path += ("[{: >3d}/{: <3d}] "
                              .format(self.__tree_path[piece_idx][1],
                                      len(self.__pieces[piece_idx].positions)))
            else:
                tree_path = tree_path + "[   /   ] "
        print(tree_path, end="\r", flush=True)

    def add_piece(self, piece):
        """Method: add a piece, with all its possible positions on the board, 
        to the puzzle piece stack"""
        # Add to piece stack
        self.__pieces.append(copy.deepcopy(piece))
        # Generate positions for the piece
        self.__pieces[-1].generate_positions(self.__board_rows, 
                                             self.__board_columns)        
        # Update the total count of combinations
        positions_count = len(self.__pieces[-1].positions)
        self.__combinations_count *= positions_count
        if self.__verbose:
            print("Info: Adding {} positions for piece '{}'"
                  .format(positions_count, self.__pieces[-1].name))    

    def solve(self):
        """Method: solve the puzzle by going trhough all combinations of pieces
           positions, moving horizontally in the tree, i.e. each time we have a
           valid combination for a piece, test it with the next piece 
           positions."""
        if self.__verbose:
            print("Info: testing {:,d} combinations of positions in total !"
                  .format(self.__combinations_count).replace(",", " "))
        start = time.time()
        # Sort the pieces stack from smallest number of positions to the 
        # biggest, to optimize tree path
        self.__pieces.sort(key=lambda piece: len(piece.positions))
        # Each position of the first piece is a tree root
        for position_idx in range(len(self.__pieces[0].positions)):          
            # Root node of the tree
            self.__tree_path = [(0, position_idx)]
            # Init the board with root position
            self.__board = numpy.copy(self.__pieces[0].positions[position_idx])
            if len(self.__pieces) == 1:
                # Only solution is board 4x4 and square piece
                # Save the tree path as a solution and break
                self.__solutions_nodes.append(self.__tree_path.copy())
                break
            # Go through the tree, starting at first position 
            # of next piece
            test_piece_idx = 1
            test_position_idx = 0
            while True:
                # backup board and add next position to board and test it
                backup_board = numpy.copy(self.__board)
                self.__board += (self.__pieces[test_piece_idx]
                                .positions[test_position_idx])
                if numpy.max(self.__board) <= 1:
                    # We have a valid combination, save the node in 
                    # tree path
                    self.__tree_path.append((test_piece_idx, 
                                            test_position_idx))
                    if self.__verbose:
                        self.__print_tree_path()
                    # Can we move to next piece ?
                    if (test_piece_idx + 1) == len(self.__pieces):
                        # No more pieces, then we have a solution
                        # Save the tree path as a solution
                        self.__solutions_nodes.append(self.__tree_path
                                                        .copy())                       
                        # Stop if we look at the first solution only
                        first_found = True
                        if self.__first:
                            break
                        # Remove the last position added
                        self.__tree_path.pop()
                        # and go backward on the path, if we can
                        node = self.__tree_path_backward()
                        if not node[0]:
                            # No more node in the path, end of the tree
                            break
                        else:
                            test_piece_idx = node[1]
                            test_position_idx = node[2]                        
                    else:
                        # Move to next piece, first position
                        test_piece_idx += 1
                        test_position_idx = 0 
                else:
                    # Not a valid combination, move to next position, 
                    # if it exists
                    if ((test_position_idx + 1) 
                        == len(self.__pieces[test_piece_idx].positions)):
                        # No more position for the piece
                        # Go backward on the path, if we can
                        node = self.__tree_path_backward()
                        if not node[0]:
                            # No more node in the path, end of the tree
                            break
                        else:
                            test_piece_idx = node[1]
                            test_position_idx = node[2]                        
                    else:
                        # Restore the board
                        self.__board = numpy.copy(backup_board)
                        test_position_idx += 1
            # Stop if we look at the first solution only
            if self.__first and first_found:
                break
        stop = time.time()
        if self.__verbose:
            print()
            print("Info: Time spent in solving puzzle: {:,.2f} secondes"
                  .format(stop - start).replace(",", " "))

    def solutions(self):
        """Method: output the solutions if we have some"""
        # Output solutions       
        for solution in self.__solutions_nodes:
            solution_label = [["" 
                               for col in range(self.__board_columns)] 
                               for row in range(self.__board_rows)]
            solution_pieces = [[0 
                                for col in range(self.__board_columns)] 
                                for row in range(self.__board_rows)]
            for node in solution:
                position = self.__pieces[node[0]].positions[node[1]]
                for row in range(self.__board_rows):
                    for column in range(self.__board_columns):
                        if position[row][column] == 1:
                            solution_label[row][column] = self.__pieces[
                                                          node[0]].label
                            solution_pieces[row][column] = node[0]
            if solution_label not in self.__solutions_label:
                # Add solution if not already existing
                self.__solutions_label.append(solution_label)
                self.__solutions_pieces.append(solution_pieces)
                print("Solution:\n--------", *solution_label, sep="\n ")
        # Report solutions
        if len(self.__solutions_label) != 0:
            print("Puzzle solved ! Found {} unique solutions"
                  .format(len(self.__solutions_label)))
        else:
            print("No solution found for the puzzle !")
            exit(0)
        # Output images if needed
        if self.__images:
            # Create directory to store the images
            try:
                os.makedirs(self.__output_dir,exist_ok=True)
            except IOError:
                print("Fatal: Can't create output directory {}"
                      .format(self.__output_dir)) 
                exit(1)
            for solution_idx, solution in enumerate(self.__solutions_pieces, 
                                                    1):
                # Draw the solution
                image = tpimages.draw_board(solution, self.__cell_size, 
                                            self.__fill_color, 
                                            self.__shape_color)
                # Save the image
                image_name = (self.__output_dir 
                              + "\\Solution #{:0>2}.png".format(solution_idx))
                try:
                    image.save(image_name)
                except:
                    print("Fatal: Can't save image {}".format(image_name)) 
