import re
import textwrap


class Comic:
    def __init__(self, title, series, volume, is_manga):
        self.title = title
        self.series = series
        self.volume = volume
        self.is_manga = is_manga

    @staticmethod
    def from_file_name(file_name, is_manga=False):
        pattern = re.compile(r"^(?P<series>.*?)(?: v(?P<volume>[0-9]+))?(?: \[(?P<title>.*?)])?\.zip$")
        match = re.match(pattern, file_name)
        if match is None:
            return None
        return Comic(
            series=match.group("series"),
            volume=match.group("volume"),
            title=match.group("title"),
            is_manga=is_manga
        )

    def print(self):
        print(textwrap.dedent(
            f"""\
            ----- Comic -----
              Series: {self.series}
              Volume: {self.volume}
              Title: {self.title}
              Manga: {"Yes" if self.is_manga else "No"}
            -----------------\
            """
        ))
