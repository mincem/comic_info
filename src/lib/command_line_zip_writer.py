import subprocess

ZIP_FORMAT = "-tzip"
NO_COMPRESSION = "-mx=0"


class CommandLineZipWriter:
    def __init__(self, zip_file_path):
        self.zip_file_path = zip_file_path

    def add(self, file_path):
        seven_zip_command = ["7z", "a", ZIP_FORMAT, NO_COMPRESSION, self.zip_file_path, file_path]
        completed_process = subprocess.run(seven_zip_command, capture_output=True)
        if completed_process.returncode != 0:
            raise Exception("Error running 7zip.")
