import re
import textwrap
from dataclasses import dataclass


@dataclass
class Comic:
    series: str
    title: str = None
    volume: int = None
    number: int = None
    is_manga: bool = False
    file_name: str = None
    writer: str = None
    penciller: str = None
    publisher: str = None
    imprint: str = None
    genre: str = None
    language_iso: str = None

    @classmethod
    def from_file_name(cls, file_name, is_manga=False):
        pattern = re.compile(
            r"^(?P<series>.*?)(?: v(?P<volume>[0-9]+)| #(?P<number>[0-9]+))?(?: \[(?P<title>.*?)])?\.zip$"
        )
        match = re.match(pattern, file_name)
        if match is None:
            return None
        volume = match.group("volume")
        number = match.group("number")
        return cls(
            series=match.group("series"),
            volume=int(volume) if volume is not None else None,
            number=int(number) if number is not None else None,
            title=match.group("title"),
            is_manga=is_manga,
            file_name=file_name,
        )

    def set_fields(self, fields: dict):
        for field_name, field_value in fields.items():
            setattr(self, field_name, field_value)

    def print(self):
        print(textwrap.dedent(
            f"""\
            ----- Comic -----
              Series: {self.series}
              Volume: {self.volume}
              Number: {self.number}
              Title: {self.title}
              Manga: {"Yes" if self.is_manga else "No"}
              Writer: {self.writer}
              Penciller: {self.penciller}
              Publisher: {self.publisher}
              Imprint: {self.imprint}
              Genre: {self.genre}
              Language: {self.language_iso}
            -----------------\
            """
        ))
