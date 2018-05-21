#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Module: Exception classes definition

Name: tperrors.py
Exception classes:
    TalosError: base class for application exceptions
    FileSystemError: errors in saving an image or stats
"""


class TalosError(Exception):
    """Exception class: base class for application exceptions

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


class FileSystemError(TalosError):
    """Exception class: raised for errors in writing on the filesystem.

    Inherit:
        TalosError
    Public members:
        Attributes:
            syserror: Exception - system exception
    Special methods:
        __init__: extend TalosError constructor
    """

    def __init__(self, message, syserror):
        """Method: extend TalosError constructor

        Inputs:
            message: string - explanation of the error
            syserror: Exception - system exception
        """

        super().__init__(message)
        self.syserror = syserror
