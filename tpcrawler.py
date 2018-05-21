#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Module: Tree crawler process and processes collection

Name: tpcrawler.py
Classes:
    CrawlersCollection: collection of crawler processes
Functions:
    crawl_tree: recursive tree crawler process
Dependencies:
    threading
    multiprocessing
    queue
    numpy
"""

import threading as td
from multiprocessing import Event, Process, Queue
from queue import Empty

import numpy


class CrawlersCollection(object):
    """Class: tree crawler processes collection

    Public members:
        Methods:
            add: add a crawler to the collection, from the given tree path
            start: start all the crawlers from the collection
            get_solutions:
    Private members:
        Attributes:
            __positions: PositionsStackCollection - puzzle collection of
                positions
            __max_depth: integer - max depth for tree crawling
            __first: boolean - stop at first solution found
            __queue: multiprocessing.Queue - communication queue for crawlers
            __found: multiprocessing.Event - solution found event for crawlers
            __crawlers: list of multiprocessing.Process - list of crawler
                processes
            __supervisor: threading.Thread - thread waiting for crawlers
                termination
            __done: threading.Event - all crawlers terminated event
        Methods:
            __supervise: watch all crawler processes for termination
    Special methods:
        __init__: override object constructor
    """

    def __init__(self, positions, max_depth, first):
        """Method: override object constructor

        Inputs:
            positions: PositionsStackCollection - puzzle collection of
                positions
            max_depth: integer - max depth for tree crawling
            first: boolean - stop at first solution found
        """

        self.__positions = positions
        self.__max_depth = max_depth
        self.__first = first
        self.__queue = Queue()
        self.__found = Event()
        self.__crawlers = []
        self.__supervisor = None
        self.__done = td.Event()

    def __supervise(self):
        """Method: send 'done' event after all crawlers terminate"""

        for crawler in self.__crawlers:
            crawler.join()
        self.__done.set()

    def add(self, tree_path):
        """Method: add a tree crawler to the collection

        Inputs:
            tree_path: list of integer tuples (row, col) - tree root
        """

        # Get the tree root position
        piece_idx = tree_path[0][0]
        position_idx = tree_path[0][1]
        board = numpy.copy(self.__positions[piece_idx][position_idx])
        # Create the crawler process and append it to the list
        crawler = Process(
            target=crawl_tree,
            args=(
                self.__positions,
                tree_path,
                board,
                self.__max_depth,
                self.__queue,
                self.__first,
                self.__found
            )
        )
        self.__crawlers.append(crawler)

    def start(self):
        """Method: start all the crawlers and the supervisor thread"""

        # Create the supervisor
        self.__supervisor = td.Thread(target=self.__supervise, daemon=True)
        # Start the crawlers
        for crawler in self.__crawlers:
            crawler.deamon = True
            crawler.start()
        # Start the supervisor
        self.__supervisor.start()

    def get_solutions(self, solutions):
        """Method: get solutions from the queue, add them to solutions
        collection, until there is no more active crawler

        Outputs:
            solutions: SolutionsCollection, puzzle collection of solutions
        """

        # Loop while we have some crawlers running
        while not self.__done.is_set():
            solution_tree_path = None
            try:
                # Try to get a solution from the queue
                solution_tree_path = self.__queue.get_nowait()
            except Empty:
                pass
            if solution_tree_path:
                # Add it to the collection if we have one
                solutions.add(solution_tree_path)
        # Wait for supervisor ending
        self.__supervisor.join()


def crawl_tree(positions, tree_path, board, max_depth, queue, first, found):
    """Function: Recursively go through the positions tree and combine them to
    determine puzzle solutions. Designed to be ran in a separate process.

    Inputs:
        positions: PositionsStackCollection - puzzle collection of positions
        tree_path: list of integer tuples (row, col) - valid tree path
        board: numpy array - puzzle board
        max_depth: integer - max depth for tree crawling
        queue: multiprocessing.Queue - communication queue for crawlers
        first: boolean - stop at first solution found
        found: multiprocessing.Event - solution found event for crawlers
    Outputs:
        tree_path: list of integer tuples (row, col) - valid tree path
        queue: multiprocessing.Queue - communication queue for crawlers
        found: multiprocessing.Event - solution found event for crawlers
    """

    current_node = tree_path[-1]
    next_piece_idx = current_node[0] + 1
    # Combine current node with all nodes (positions) of next piece
    for position_idx, position in enumerate(positions[next_piece_idx]):
        # Exits immediately, if we have to stop after first solution found
        if first:
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
                # solution. Send copy of valid tree path to main process.
                queue.put(tree_path.copy())
                # If we have to stop after first solution found, tell other
                # processes that a solution has been found
                if first:
                    found.set()
            else:
                # Move to the next piece
                crawl_tree(
                    positions,
                    tree_path,
                    board,
                    max_depth,
                    queue,
                    first,
                    found
                )
            # Restore tree path to current node
            tree_path.pop()
        # Restore board to previous state and move to next position
        board = numpy.copy(backup_board)
