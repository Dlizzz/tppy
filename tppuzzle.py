#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Name: tppuzzle.py
    Description:
        talos-puzzle puzzle definition
"""
import os
import numpy
import time
from PIL import ImageColor
from threading import Thread
from tperrors import ImageError
from tpsolutions import SolutionsCollection
from tppieces import PiecesCollection
from tppositions import PositionsStackCollection


class Puzzle(object):
    """Class: game board and stack of solutions"""

    def __init__(self, args):
        """Constructor: init the puzzle with rows x columns dimension"""
        # Protected members
        # Do we have to be verbose
        self.__verbose = args.verbose
        # Do we stop at first solution found
        self.__first = args.first
        # Images output
        self.__save_images = args.images
        self.__cell_size = args.cell_size
        self.__fill_color = ImageColor.getrgb(args.fill_color)
        self.__shape_color = ImageColor.getrgb(args.shape_color)
        self.__output_dir = (
            args.output_dir
            + "\\Board {}Rx{}C - {}LR {}LL {}SR {}SL {}TE {}BA {}SQ"
            .format(
                args.rows,
                args.columns,
                args.l_right,
                args.l_left,
                args.step_right,
                args.step_left,
                args.tee,
                args.bar,
                args.square
            )
        )
        # Collection of pieces
        self.__pieces = PiecesCollection()
        # Collection of positions per pieces
        self.__positions = PositionsStackCollection()
        # Collection of solutions
        self.__solutions = SolutionsCollection()
        # Properties (read only)
        # Game board dimensions
        self.__board_rows = args.rows
        self.__board_columns = args.columns

    @property
    def board_rows(self):
        return self.__board_rows

    @property
    def board_columns(self):
        return self.__board_columns

    def __print_config(self):
        """Method: print puzzle configuration"""
        print(
            "Info: Puzzle board is {} rows x {} columns (size = {})"
            .format(
                self.__board_rows,
                self.__board_columns,
                self.__board_rows * self.__board_columns
            )
        )
        print("Info: Solving puzzle with the following pieces set:")
        for piece_idx, piece in enumerate(self.__pieces):
            print(
                "\t{: >10} with {:0>3} positions"
                .format(piece.name, len(self.__positions[piece_idx]))
            )
        print(
            "Info: Testing {:,d} combinations of positions"
            .format(self.__positions.combinations_count)
            .replace(",", " ")
        )
        if self.__save_images:
            print(
                "Info: Solutions image will be generated in {} with a cell "
                "size of {}."
                .format(self.__output_dir, self.__cell_size)
            )

    def add_piece(self, piece):
        """Method: add a piece to the collection
        """
        # Append to pieces collection
        self.__pieces.append(piece)

    def solve(self):
        """Method (public):
           Solve the puzzle by going trhough all combinations of pieces
           positions, moving horizontally in the tree, i.e. each time we have a
           valid combination for a piece, test it with the next piece
           positions.
        """
        # Generate positions tree
        for piece in self.__pieces:
            self.__positions.add(
                piece,
                self.__board_rows,
                self.__board_columns
            )
        # Optimize positions tree
        self.__positions.optimize()
        # Print config if needed
        if self.__verbose:
            self.__print_config()
        # Start crawling the tree
        start = time.time()
        # Maximum depth to reach in the tree (one level before the last one)
        max_depth = len(self.__pieces) - 2
        if max_depth < 0 and self.__positions.combinations_count > 0:
            # We have only one piece (a square or a bar) with one position and
            # at least one. Then we have all the solutions
            self.__solutions.add(
                self.__positions,
                self.__board_rows,
                self.__board_columns,
                [(0, 0)]
            )
        else:
            # If we need to stop after first solution found
            if self.__first:
                # Create a signal thread on the solution collection, which
                # will stop the crawlers after the first solution found
                signaler = Thread(target=self.__solutions.solution_found)
                signaler.start()
            # Stack of crawler threads
            crawler_threads = []
            # Each position of the first piece is a tree root
            for position_idx, position in enumerate(self.__positions[0]):
                # Init tree path with root node
                tree_path = [(0, position_idx)]
                # Init the board with root position
                board = numpy.copy(position)
                # Create the crawler_thread
                crawler = Thread(
                    target=self.__positions.crawl_tree,
                    args=(
                        self.__solutions,
                        tree_path,
                        board,
                        max_depth
                    )
                )
                crawler_threads.append(crawler)
            # Start the crawler
            for crawler in crawler_threads:
                crawler.start()
            if self.__first:
                # Wait for the waiter to terminate
                signaler.join()
            # Wait for all threads to terminate
            for crawler in crawler_threads:
                crawler.join()
        stop = time.time()
        if self.__verbose:
            print("Info: Time spent in solving puzzle: {:,.2f} secondes"
                  .format(stop - start).replace(",", " "))

    def solutions(self):
        """Method: output the solutions if we have some"""
        # Report solutions
        if len(self.__solutions) != 0:
            print(
                "Puzzle solved ! Found {} unique solutions"
                .format(len(self.__solutions))
            )
            self.__solutions.echo()
        else:
            print("No solution found for the puzzle !")
            exit(0)
        # Save images if needed
        if self.__save_images:
            # Create directory to store the images
            try:
                os.makedirs(self.__output_dir, exist_ok=True)
            except OSError as err:
                print("Fatal: Can\'t create output directory {}."
                      " System message is: "
                      .format(self.__output_dir), err)
                exit(1)
            # Draw all solutions
            self.__solutions.draw(self.__cell_size, self.__fill_color,
                                  self.__shape_color)
            # Save all solutions
            try:
                self.__solutions.save(self.__output_dir)
            except ImageError as err:
                print(err.message, " with system error: ", err.syserror)
                exit(1)
