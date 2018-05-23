#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Exceptions classes definition

Name: tperrors.py
Exception classes:
    TalosError: base class for tppy exceptions
    TalosArgumentError: errors in command line arguments
    TalosFileSystemError: errors in saving an image or stats
"""


class TalosError(Exception):
    """Base class for tppy exceptions

    Inherit:
        Exception
    Public members:
        Attributes:
            message: string - explanation of the error
            syserror: Exception - system exception
    Special methods:
        __init__: override Exception constructor
    """

    def __init__(self, message):
        """Method: extend Exception constructor

        Inputs:
            message: string - explanation of the error
        """

        self.message = message


class TalosArgumentError(TalosError):
    """Command line arguments parsing exceptions

    Inherit:
        TalosError
    Public members:
        Attributes:
            message: string - explanation of the error
            argument: string - the faulty argument
    Special methods:
        __init__: extend TalosError constructor
    """

    def __init__(self, message, argument):
        """Extend TalosError constructor

        Inputs:
            argument: string - the faulty argument
            message: string - explanation of the error
        """

        super().__init__(message)
        self.argument = argument


class TalosFileSystemError(TalosError):
    """Filesystem access exceptions

    Inherit:
        TalosError
    Public members:
        Attributes:
            syserror: Exception - system exception
    Special methods:
        __init__: extend TalosError constructor
    """

    def __init__(self, message, syserror):
        """Extend TalosError constructor

        Inputs:
            message: string - explanation of the error
            syserror: Exception - system exception
        """

        super().__init__(message)
        self.syserror = syserror
