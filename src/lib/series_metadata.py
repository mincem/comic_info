import json
import os
import re
import unicodedata

FILE_NAME = "comic_metadata.json"

# Fields copied from comic_metadata.json into Comic. Other keys (country, notes) are ignored.
FIELDS = ("writer", "penciller", "publisher", "imprint", "genre", "language_iso")


def normalize(text: str) -> str:
    """Same as normalize in ai_folder_organizer (src/lib/command.py). Keep them in sync."""
    without_accents = ''.join(c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c))
    return re.sub(r'\W', '', without_accents.casefold())


class SeriesMetadata:
    """Series metadata from <directory>/comic_metadata.json, written by ai_folder_organizer."""

    def __init__(self, directory: str):
        self.path = os.path.join(directory, FILE_NAME)
        self.index = {}
        self.missing_series = set()
        self.found = os.path.exists(self.path)
        if not self.found:
            print(f"Info: no {FILE_NAME} in {directory}, no series metadata will be added.")
            return
        for series, item in self._load().items():
            key = normalize(series)
            if key in self.index:
                print(f"Warning: '{series}' in {FILE_NAME} matches the same series as "
                      f"'{self.index[key][0]}', ignoring it.")
                continue
            self.index[key] = (series, self._fields(series, item))

    def get(self, series: str) -> dict:
        """Fields for the series, without the null ones. Empty when there's no metadata for it."""
        if not self.found:
            return {}
        entry = self.index.get(normalize(series))
        if entry is None:
            if series not in self.missing_series:
                self.missing_series.add(series)
                print(f"Warning: no metadata for series '{series}' in {FILE_NAME}.")
            return {}
        return entry[1]

    def _load(self) -> dict:
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except (OSError, json.JSONDecodeError) as e:
            raise ValueError(f"Could not read {self.path}: {e}") from e
        if not isinstance(data, dict) or not all(isinstance(item, dict) for item in data.values()):
            raise ValueError(f"Could not read {self.path}: expected a JSON object keyed by series name, "
                             "with an object for each series")
        return data

    def _fields(self, series: str, item: dict) -> dict:
        fields = {}
        for name in FIELDS:
            value = item.get(name)
            if value is None:
                continue
            if not isinstance(value, str):
                raise ValueError(f"Could not read {self.path}: '{name}' of '{series}' must be text or null")
            if value.strip():
                fields[name] = value.strip()
        return fields
