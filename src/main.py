from argparse import ArgumentParser

from lib.command import Command

STARTING_DIRS = []

if __name__ == '__main__':
    parser = ArgumentParser(description='Add ComicInfo file to comic book Zip files.')
    parser.add_argument(
        '--path',
        help='path to the starting directory'
    )
    parser.add_argument(
        '--manga',
        action='store_true',
        help='treat comics as manga'
    )
    parser.add_argument(
        '--field',
        nargs=2,
        action='append',
        metavar=('KEY', 'VALUE'),
        help='Add a custom metadata field. Can be used multiple times. Example: --field publisher Marvel'
    )

    arguments = parser.parse_args()
    custom_fields = dict(arguments.field) if arguments.field else {}

    if arguments.path is None:
        for starting_dir in STARTING_DIRS:
            Command(starting_dir=starting_dir, is_manga=arguments.manga, **custom_fields).execute()
    else:
        Command(starting_dir=arguments.path, is_manga=arguments.manga, **custom_fields).execute()
