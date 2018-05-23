#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Define the Puzzle

Name: tppuzzle.py
Classes:
    Puzzle: the Puzzle
Dependencies:
    pathlib
    socket
    time
    PIL
    tpcrawler
    tperrors
    tppieces
    tppositions
    tpsolutions
"""

from pathlib import Path
from socket import gethostname
from time import strftime, time

from PIL import ImageColor

from tpcrawler import CrawlersCollection
from tperrors import TalosFileSystemError
from tppieces import PiecesCollection
from tppositions import PositionsStackCollection
from tpsolutions import SolutionsCollection


class Puzzle(object):
    """The puzzle

    Private members:
        Attributes:
            __verbose: boolean - print verbose messages if True
            __first: boolean - stop after first solution found
            __stats: boolean - save stats in CSV file
            __config: string - puzzle configuration in one line
            __save_images: boolean - save solutions PNG images if True
            __cell_size: integer - size in pixels of a board cell
            __fill_color: RGB tuples of integer - color of the cell
            __shape_color: RGB tuples of integer - color of the cell shape
            __output_dir: pathlib.Path - directory where to save the images
            __board_rows: integer - # of rows on the board
            __board_columns: integer - # of columns on the board
            __pieces: PiecesCollection - collection of pieces
            __positions: PositionsStackCollection - collection of positions
            __solutions: SolutionsCollection - collection of solutions
        Methods:
            __print_config: Print puzzle configuration
            __save_stats: Save puzzle solving statistics to CSV file
    Public members:
        Methods:
            add_piece: Add a piece to the puzzle set of pieces
            solve: Solve the puzzle
            solutions: Output and save the solutions if we have some
    Special methods:
        __init__: override object constructor
    Properties:
        board_rows: integer - # of rows on the board
        board_columns: integer - # of columns on the board
    Exceptions:
        TalosFileSystemError: errors in saving stats or images
    """

    def __init__(self, args):
        """Puzzle initialization from the given arguments

        Inputs:
            args: argparse.args - command line arguments
        """

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
        # Game board dimensions
        self.__board_rows = args.rows
        self.__board_columns = args.columns
        # Collection of pieces
        self.__pieces = PiecesCollection()
        # Collection of positions per pieces
        self.__positions = PositionsStackCollection()
        # Collection of solutions
        self.__solutions = SolutionsCollection(
            self.__positions,
            self.__board_rows,
            self.__board_columns
        )

    @property
    def board_rows(self):
        """integer - # of rows on the board"""

        return self.__board_rows

    @property
    def board_columns(self):
        """integer - # of columns on the board"""

        return self.__board_columns

    def __print_config(self):
        """Print puzzle configuration"""

        print(
            "Info: Puzzle board is {} rows x {} columns (size = {})"
            .format(
                self.__board_rows,
                self.__board_columns,
                self.__board_rows * self.__board_columns
            )
        )
        print("Info: Solving puzzle with the following pieces set:")
        for positions in self.__positions:
            print(
                "\t{: >10} with {:0>3} positions"
                .format(positions.piece.name, len(positions))
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
        """Save puzzle solving statistics to CSV file

        Inputs:
            time_spend: integer - time spend in seconds
        Exceptions:
            TalosFileSystemError: errors in saving stats
        """

        stats_file = Path.cwd() / "talos-puzzle-stats.csv"
        puzzle_id = "P" + self.__config.replace(",", "")
        stats_line = (
            gethostname()
            + ","
            + strftime("%d/%m/%Y %H:%M:%S")
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
                raise TalosFileSystemError(message, err)
        else:
            try:
                with stats_file.open("a") as f:
                    f.write(stats_line)
            except OSError as err:
                message = "Error: Can't save stats in file " + str(stats_file)
                raise TalosFileSystemError(message, err)

    def add_piece(self, piece):
        """Add a piece to the puzzle set of pieces

        Inputs:
            piece: Piece - the piece to add
        """

        # Append to pieces collection
        self.__pieces.append(piece)

    def solve(self):
        """Solve the puzzle"""

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
        start = time()
        # Maximum depth to reach in the tree (one level before the last one)
        max_depth = len(self.__pieces) - 2
        if max_depth < 0 and self.__positions.combinations_count > 0:
            # We have only one piece (a square or a bar) with one position and
            # at least one. Then we have all the solutions
            self.__solutions.add([(0, 0)])
        else:
            # Collection of crawler subprocesses
            crawlers = CrawlersCollection(
                self.__positions,
                max_depth,
                self.__first
            )
            # Each position of the first piece is a tree root
            for position_idx in range(len(self.__positions[0])):
                # Init tree path with root node
                tree_path = [(0, position_idx)]
                # Add crawler to the collection
                crawlers.add(tree_path)
            # Start the crawlers
            crawlers.start()
            # Get the solutions
            crawlers.get_solutions(self.__solutions)
        stop = time()
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
            except TalosFileSystemError as err:
                print(err.message, " with system error: ", err.syserror)

    def solutions(self):
        """Output and save the solutions if we have some"""

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
            except TalosFileSystemError as err:
                print(err.message, " with system error: ", err.syserror)
                exit(1)
