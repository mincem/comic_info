import re
import textwrap
from dataclasses import dataclass


@dataclass
class Comic:
    series: str
    title: str = None
    volume: str = None #TODO: Integers
    number: str = None
    is_manga: bool = False
    file_name: str = None

    @classmethod
    def from_file_name(cls, file_name, is_manga=False):
        pattern = re.compile(
            r"^(?P<series>.*?)(?: v(?P<volume>[0-9]+)| #(?P<number>[0-9]+))?(?: \[(?P<title>.*?)])?\.zip$"
        )
        match = re.match(pattern, file_name)
        if match is None:
            return None
        return cls(
            series=match.group("series"),
            volume=match.group("volume"),
            number=match.group("number"),
            title=match.group("title"),
            is_manga=is_manga,
            file_name=file_name,
        )

    def print(self):
        print(textwrap.dedent(
            f"""\
            ----- Comic -----
              Series: {self.series}
              Volume: {self.volume}
              Number: {self.number}
              Title: {self.title}
              Manga: {"Yes" if self.is_manga else "No"}
            -----------------\
            """
        ))
