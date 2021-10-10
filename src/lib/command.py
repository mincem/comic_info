import os

from .comic import Comic
from .comic_info_writer import ComicInfoWriter
from .zip_writer import ZipWriter


class Command:
    def __init__(self, starting_dir):
        self.starting_dir = starting_dir

    def execute(self):
        _start_dir, directories, file_names = next(os.walk(self.starting_dir))
        print(directories)
        print(file_names)
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
        print(f"File path: {file_path}")
        comic_info_file_path = ComicInfoWriter(comic, self.starting_dir).write()
        ZipWriter(file_path).add(comic_info_file_path)
