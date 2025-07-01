import os

from .comic import Comic
from .comic_info_writer import ComicInfoWriter
from .command_line_zip_writer import CommandLineZipWriter
from .zip_writer import ZipWriter

ONE_SHOTS_FOLDER = "!One-shots"


def running_on_windows():
    return os.name == 'nt'


class Command:
    def __init__(self, starting_dir, is_manga = False):
        self.starting_dir = starting_dir
        self.is_manga = is_manga

    def execute(self):
        try:
            _start_dir, directories, file_names = next(os.walk(self.starting_dir))
        except StopIteration:
            raise Exception(f'Directory "{self.starting_dir}" not found.') from None
        for file_name in file_names:
            if file_name.endswith(".zip"):
                comic = Comic.from_file_name(file_name, is_manga=self.is_manga)
                if comic:
                    self.process_comic(comic, self.starting_dir)
                    self.move_to_subfolder(comic, self.starting_dir)
        for directory in directories:
            subfolder_path = os.path.join(self.starting_dir, directory)
            _, _, file_names = next(os.walk(subfolder_path))
            for file_name in file_names:
                if file_name.endswith(".zip"):
                    comic = Comic.from_file_name(file_name, is_manga=self.is_manga)
                    if comic:
                        self.process_comic(comic, subfolder_path)

    def process_comic(self, comic: Comic, directory):
        print()
        print(f"File: {comic.file_name}")
        comic.print()
        file_path = os.path.join(directory, comic.file_name)
        comic_info_file_path = ComicInfoWriter(comic, directory).write()
        self.add_file_to_zip(file_path, comic_info_file_path)
        os.remove(comic_info_file_path)

    def move_to_subfolder(self, comic: Comic, directory):
        target_folder_name = ONE_SHOTS_FOLDER if comic.volume is None and comic.title is None else comic.series
        target_folder_path = os.path.join(directory, target_folder_name)

        if not os.path.exists(target_folder_path):
            os.makedirs(target_folder_path)
            print(f"Created folder: {target_folder_name}")

        source_path = os.path.join(directory, comic.file_name)
        target_path = os.path.join(target_folder_path, comic.file_name)
        os.rename(source_path, target_path)
        print(f"Moved '{comic.file_name}' to '{target_folder_name}/'")

    @staticmethod
    def add_file_to_zip(zip_file_path, comic_info_file_path):
        if running_on_windows():
            CommandLineZipWriter(zip_file_path).add(comic_info_file_path)
        else:
            ZipWriter(zip_file_path).add(comic_info_file_path)
