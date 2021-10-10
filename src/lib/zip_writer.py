import os
from zipfile import ZipFile


class ZipWriter:
    def __init__(self, zip_file_path):
        self.zip_file_path = zip_file_path

    def add(self, file):
        with ZipFile(self.zip_file_path, "a") as zip_file:
            zip_file.write(file, os.path.basename(file))
