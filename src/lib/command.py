import os

from .comic import Comic
from .comic_info_writer import ComicInfoWriter
from .zip_writer import ZipWriter
from .command_line_zip_writer import CommandLineZipWriter


def running_on_windows():
    return os.name == 'nt'


class Command:
    def __init__(self, starting_dir):
        self.starting_dir = starting_dir

    def execute(self):
        try:
            _start_dir, directories, file_names = next(os.walk(self.starting_dir))
        except StopIteration:
            raise Exception(f'Directory "{self.starting_dir}" not found.') from None
        for file_name in file_names:
            self.process_file(file_name)

    def process_file(self, file_name):
        if not file_name.endswith(".zip"):
            return
        print()
        print(f"File: {file_name}")
        comic = Comic.from_file_name(file_name)
        if comic is None:
            return
        comic.print()
        file_path = os.path.join(self.starting_dir, file_name)
        comic_info_file_path = ComicInfoWriter(comic, self.starting_dir).write()
        self.add_file_to_zip(file_path, comic_info_file_path)
        os.remove(comic_info_file_path)

    @staticmethod
    def add_file_to_zip(zip_file_path, comic_info_file_path):
        if running_on_windows():
            CommandLineZipWriter(zip_file_path).add(comic_info_file_path)
        else:
            ZipWriter(zip_file_path).add(comic_info_file_path)
