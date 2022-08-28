#!/usr/bin/env python3


import re
import os
import sys
import argparse
from termcolor import colored
from typing import Sequence


def is_colon_path(text: str) -> bool:
    return text.find(':') != -1 and text.find('/') != -1


def shall_include(args, name: str, value: str) -> bool:
    return ((args.VARIABLE and name in args.VARIABLE) or
            any([re.search(rx, name) for rx in args.regex]))


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Pretty print environment variables")
    parser.add_argument('VARIABLE', type=str, nargs='*', help='Print VARIABLE')
    parser.add_argument('-r', '--regex', metavar='RX', type=str, action='append',
                        help='Print variables matching regex')
    return parser.parse_args(argv[1:])


def main(argv: Sequence[str]) -> None:
    args = parse_args(argv)

    variables = [ (name, value)
                  for (name, value) in os.environ.items()
                  if shall_include(args, name, value) ]

    for name, value in variables:
        if is_colon_path(value):
            print(colored(name, 'green'), "=")
            for val in value.split(':'):
                print(f"  {val}")
        else:
            print(f"{colored(name, 'green')} = {value}")


def main_entrypoint() -> None:
    main(sys.argv)


# EOF #

