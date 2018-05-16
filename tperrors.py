#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Name: tperrorss.py
    Description:
        talos-puzzle errors definition
"""


class ImageError(Exception):
    """Exception raised for errors in saving an image.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, message, syserror):
        self.syserror = syserror
        self.message = message


class StatsError(Exception):
    """Exception raised for errors in saving stats.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, message, syserror):
        self.syserror = syserror
        self.message = message
