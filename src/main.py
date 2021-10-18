import sys
from argparse import ArgumentParser

from lib.command import Command

STARTING_DIRS = []

if __name__ == '__main__':
    parser = ArgumentParser(description='Add ComicInfo file to comic book Zip files.')
    parser.add_argument('startingDirectory', nargs="?", help='Path to the starting directory.')
    arguments = parser.parse_args(sys.argv[1:])
    if arguments.startingDirectory is None:
        for starting_dir in STARTING_DIRS:
            Command(starting_dir=starting_dir).execute()
    else:
        Command(starting_dir=arguments.startingDirectory).execute()
