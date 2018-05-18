#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Name: tppuzzle.py
    Description:
        talos-puzzle puzzle definition
"""
import socket
import time
import multiprocessing as mp
from pathlib import Path

import numpy
from PIL import ImageColor

import tpcrawler
import tpcollector
from tperrors import ImageError, StatsError
from tppieces import PiecesCollection
from tppositions import PositionsStackCollection
from tpsolutions import SolutionsCollection


class Puzzle(object):
    """Class: game board and stack of solutions"""

    def __init__(self, args):
        """Constructor: init the puzzle with rows x columns dimension"""
        # Protected members
        # Do we have to be verbose
        self.__verbose = args.verbose
        # Do we stop at first solution found
        self.__first = args.first
        # Do we save puzzle solving statistics
        self.__stats = args.stats
        # Puzzle configuration for stats output
        self.__config = (
            "{:0>2},{:0>2},{:0>2},{:0>2},{:0>2},{:0>2},{:0>2},{:0>2},{:0>2}"
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
        # Images output
        self.__save_images = args.images
        self.__cell_size = args.cell_size
        self.__fill_color = ImageColor.getrgb(args.fill_color)
        self.__shape_color = ImageColor.getrgb(args.shape_color)
        self.__output_dir = (
            Path(args.output_dir)
            / "Board {}Rx{}C - {}LR {}LL {}SR {}SL {}TE {}BA {}SQ"
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
        # Game board dimensions
        self.__board_rows = args.rows
        self.__board_columns = args.columns
        # Subprocesses coordination
        self.__queue = mp.Queue()
        self.__found = mp.Event()

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

    def __save_stats(self, time_spend):
        """
        Method: Save puzzle solving statistics to CSV file
        """
        stats_file = Path.cwd() / "talos-puzzle-stats.csv"
        puzzle_id = "P" + self.__config.replace(",", "")
        stats_line = (
            socket.gethostname()
            + ","
            + time.strftime("%d/%m/%Y %H:%M:%S")
            + ","
            + puzzle_id
            + ","
            + self.__config
            + ","
            + str(self.__positions.combinations_count)
            + ","
            + str(len(self.__solutions))
            + ","
            + time_spend
            + "\n"
        )
        if not stats_file.is_file():
            try:
                with stats_file.open("w") as f:
                    f.write(
                        "Hostname,"
                        "Date,"
                        "Id,"
                        "Rows,"
                        "Columns,"
                        "L Right,"
                        "L Left,"
                        "Step Right,"
                        "Step Left,"
                        "Tee,"
                        "Bar,"
                        "Square,"
                        "Combinations,"
                        "Solutions,"
                        "Elapsed Time\n"
                    )
                    f.write(stats_line)
            except OSError as err:
                message = "Error: Can't create stats file " + str(stats_file)
                raise StatsError(message, err)
        else:
            try:
                with stats_file.open("a") as f:
                    f.write(stats_line)
            except OSError as err:
                message = "Error: Can't save stats in file " + str(stats_file)
                raise StatsError(message, err)

    def add_piece(self, piece):
        """
        Method: add a piece to the collection
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
            # All processes will be spawned
            mp.set_start_method("spawn")
            # Create the solutions collector process and start it
            collector = mp.Process(
                target=tpcollector.collector,
                args=(
                    self.__solutions,
                    self.__queue,
                    self.__found,
                    self.__first
                )
            )
            collector.deamon = True
            collector.start()
            # Stack of crawler subprocesses
            crawlers = []
            # Each position of the first piece is a tree root
            for position_idx, position in enumerate(self.__positions[0]):
                # Init tree path with root node
                tree_path = [(0, position_idx)]
                # Init the board with root position
                board = numpy.copy(position)
                # Create the crawler subprocess
                crawler = mp.Process(
                    target=tpcrawler.crawler,
                    args=(
                        self.__positions,
                        tree_path,
                        board,
                        max_depth,
                        self.__queue,
                        self.__found
                    )
                )
                crawlers.append(crawler)
            # Start the crawlers
            for crawler in crawlers:
                crawler.deamon = True
                crawler.start()
            




            if self.__first:
                
                # Wait for the waiter to terminate
                signaler.join()
            # Wait for all threads to terminate
            for crawler in crawler_threads:
                crawler.join()
        stop = time.time()
        if self.__verbose:
            print(
                "Info: Time spent in solving puzzle: {:,.2f} secondes"
                .format(stop - start).replace(",", " ")
            )
        if self.__stats:
            try:
                self.__save_stats(
                    "{:,.2f}"
                    .format(stop - start).replace(",", " ")
                )
            except StatsError as err:
                print(err.message, " with system error: ", err.syserror)

    def solutions(self):
        """Method: output the solutions if we have some"""
        # Report solutions
        if len(self.__solutions) != 0:
            if self.__first:
                message = "Puzzle solved !"
            else:
                message = (
                    "Puzzle solved ! Found {} unique solutions"
                    .format(len(self.__solutions))
                )
            print(message)
            self.__solutions.echo()
        else:
            print("No solution found for the puzzle !")
            exit(0)
        # Save images if needed
        if self.__save_images:
            # Create directory to store the images
            try:

                self.__output_dir.mkdir(parents=True, exist_ok=True)
            except OSError as err:
                print(
                    "Fatal: Can\'t create output directory {} to save images."
                    " System message is: "
                    .format(str(self.__output_dir), err)
                )
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
