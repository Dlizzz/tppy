#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Name: tpcrawler.py
    Description:
        talos-puzzle tree crawler collection definition and crawler process
"""

import threading as td
from multiprocessing import Event, Process, Queue
from queue import Empty

import numpy


class CrawlersCollection(object):
    """ Class: tree crawler collection """
    def __init__(self, positions, max_depth, first):
        self.__positions = positions
        self.__max_depth = max_depth
        self.__first = first
        # Subprocesses coordination
        self.__queue = Queue()
        self.__found = Event()
        # Stack of crawlers
        self.__crawlers = []
        # Supervisor thread
        self.__supervisor = None
        self.__done = td.Event()

    def __supervise(self):
        """
        Method (protected): supervise the crawlers and raise the done event
        when all crawlers have terminated
        """
        for crawler in self.__crawlers:
            crawler.join()
        self.__done.set()

    def add(self, tree_path):
        """ Method: add a tree crawler to the collection """
        # Get the tree root position
        piece_idx = tree_path[0][0]
        position_idx = tree_path[0][1]
        board = numpy.copy(self.__positions[piece_idx][position_idx])
        # Create the crawler subprocess
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
        """ Method: start all the crawlers """
        # Create the supervisor
        self.__supervisor = td.Thread(target=self.__supervise, daemon=True)
        # Start the crawlers
        for crawler in self.__crawlers:
            crawler.deamon = True
            crawler.start()
        # Start the supervisor
        self.__supervisor.start()

    def get_solutions(self, solutions):
        """
        Method: get the next solution in the queue, add it to the given
        solutions collection, until there is no more active crawler
        """
        while not self.__done.is_set():
            solution_tree_path = None
            try:
                solution_tree_path = self.__queue.get_nowait()
            except Empty:
                pass
            if solution_tree_path:
                solutions.add(solution_tree_path)
        # Wait supervisor ending
        self.__supervisor.join()


def crawl_tree(positions, tree_path, board, max_depth, queue, first, found):
    """
    Function: Recursive function to go through the positions
    tree and combine them to determine puzzle solutions.
    Function is designed to be run in a subprocess.
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
