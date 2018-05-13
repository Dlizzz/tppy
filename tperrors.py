#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Name: tperrorss.py       
    Description:
        talos-puzzle errors definition
"""


class TPError(Exception):
    """Class: Base class for exceptions in this module."""
    pass


class ImageError(TPError):
    """Exception raised for errors in saving an image.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, message, syserror):
        self.syserror = syserror
        self.message = message
