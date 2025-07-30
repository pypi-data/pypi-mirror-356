import argparse
import os

from .pprint_stat import (
    get_values,
    generate_mapping,
    print_table
)

def initialize_args():
    parser = argparse.ArgumentParser(
                    prog='pprint-stat',
                    description='pretty print the /proc/[pid]/stat file',
                    # epilog='Text at the bottom of help'
                    )

    parser.add_argument(
        "pid", 
        nargs="?",
        default=str(os.getpid()),
        help="the pid of the process (default: %(default)s)"
        )

    args = parser.parse_args()
    return args

def app():
    args = initialize_args()
    vals = get_values(args.pid)
    mapping = generate_mapping(vals)
    print_table(mapping)

if __name__ == "__main__":
    app()

