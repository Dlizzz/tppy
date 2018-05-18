#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Name: tpcollector.py
    Description:
        talos-puzzle solutions collector sub-process definition
"""


def collector(solutions, queue, found, first):
    """
    Function : Collect the solution from the crawlers through the queue and add
    them to the Solutions collection.
    Function is designed to be run as a subprocess
    """

    queue.get()