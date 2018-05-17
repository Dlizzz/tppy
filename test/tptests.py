#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Name: tptests.py
    Description:
        talos-puzzle testing
"""

import os
import sys
from pathlib import Path

common_args = "--verbose --stats --images"

test_configs = [
    [
        "--rows",
        "1",
        "--columns",
        "4",
        "--l-right",
        "0",
        "--l-left",
        "0",
        "--step-right",
        "0",
        "--step-left",
        "0",
        "--tee",
        "0",
        "--bar",
        "1",
        "--square",
        "0",
    ],
    [
        "--rows",
        "2",
        "--columns",
        "2",
        "--l-right",
        "0",
        "--l-left",
        "0",
        "--step-right",
        "0",
        "--step-left",
        "0",
        "--tee",
        "0",
        "--bar",
        "0",
        "--square",
        "1",
    ],
    [
        "--rows",
        "4",
        "--columns",
        "2",
        "--l-right",
        "2",
        "--l-left",
        "0",
        "--step-right",
        "0",
        "--step-left",
        "0",
        "--tee",
        "0",
        "--bar",
        "0",
        "--square",
        "0",
    ],
    [
        "--rows",
        "4",
        "--columns",
        "7",
        "--l-right",
        "1",
        "--l-left",
        "1",
        "--step-right",
        "0",
        "--step-left",
        "2",
        "--tee",
        "2",
        "--bar",
        "1",
        "--square",
        "0",
    ],
    [
        "--first",
        "--rows",
        "4",
        "--columns",
        "7",
        "--l-right",
        "1",
        "--l-left",
        "1",
        "--step-right",
        "0",
        "--step-left",
        "2",
        "--tee",
        "2",
        "--bar",
        "1",
        "--square",
        "0",
    ],
]


def main():
    """ Script main function """
    try:
        script = Path("../talos-puzzle.py").resolve(strict=True)
    except FileNotFoundError:
        print("Fatal: Can't find talos-puzzle.py script.")
        exit(1)
    for config in test_configs:
        command = (
            sys.executable
            + " "
            + str(script)
            + " "
            + common_args
            + " "
            + " ".join(config)
        )
        os.system(command)


if __name__ == "__main__":
    main()
