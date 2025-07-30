"""
Testing args
"""
#  Copyright (c) 2024.
#  Creative Commons 4 for original code
#  GPL3 for rewrite

import argparse


def list_of(*args):
    return list(args)


def main() -> None:
    arg_parser = argparse.ArgumentParser(description="load wn and syntagnet from yaml, merge and save")
    arg_parser.add_argument('arg1', type=str, help='required/positional')
    arg_parser.add_argument('arg2', type=str, nargs='?', default=None, help='optional/positional')
    arg_parser.add_argument('--opt', action=argparse.BooleanOptionalAction, help='switch')
    arg_parser.add_argument('--opt2', action='store_true', default=False, help='model to use')
    arg_parser.add_argument('--opt3', default=None, help='model to use')

    for cl in (
            list_of('A1', 'A2'),
            list_of('A1', '--opt'),
            list_of('--opt', 'A1'),
            list_of('A1', '--opt', '--opt2'),
            list_of('A1', '--opt', '--opt2', '--opt3', 'extra'),
    ):
        print(cl)
        args = arg_parser.parse_args(cl)
        print(args)


if __name__ == '__main__':
    main()
