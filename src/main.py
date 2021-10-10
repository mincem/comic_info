import sys
from argparse import ArgumentParser

from lib.command import Command

if __name__ == '__main__':
    parser = ArgumentParser(description='Add ComicInfo file to comic book Zip files.')
    parser.add_argument('startingDirectory', help='Path to the starting directory.')
    arguments = parser.parse_args(sys.argv[1:])
    Command(starting_dir=arguments.startingDirectory).execute()
