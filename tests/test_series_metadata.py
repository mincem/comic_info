import json

import pytest

from src.lib.comic import Comic
from src.lib.comic_info_writer import ComicInfoWriter
from src.lib.command import Command
from src.lib.series_metadata import FILE_NAME, SeriesMetadata, normalize

SOME_SERIES = {
    "country": "XX", "writer": "Some Writer", "penciller": "Some Penciller", "publisher": "Some Publisher",
    "imprint": None, "genre": "Genre A, Genre B", "language_iso": "xx", "notes": "Some note",
}


def write_json(directory, data):
    (directory / FILE_NAME).write_text(json.dumps(data), encoding="utf-8")


def test_normalize():
    assert normalize("Some Series!") == normalize("some series")
    assert normalize("Sérïes: Ñame") == normalize("Series Name")


def test_get_matches_normalized_name_and_skips_null_and_extra_keys(tmp_path):
    write_json(tmp_path, {"Some Series": SOME_SERIES})
    metadata = SeriesMetadata(str(tmp_path))
    assert metadata.get("SOME series") == {
        "writer": "Some Writer", "penciller": "Some Penciller", "publisher": "Some Publisher",
        "genre": "Genre A, Genre B", "language_iso": "xx",
    }


def test_missing_file_is_info_only(tmp_path, capsys):
    metadata = SeriesMetadata(str(tmp_path))
    assert metadata.get("Any Series") == {}
    output = capsys.readouterr().out
    assert output.startswith("Info:")
    assert "Warning" not in output


def test_missing_series_warns_once(tmp_path, capsys):
    write_json(tmp_path, {"Some Series": SOME_SERIES})
    metadata = SeriesMetadata(str(tmp_path))
    assert metadata.get("Other Series") == {}
    assert metadata.get("Other Series") == {}
    assert capsys.readouterr().out.count("Warning: no metadata for series 'Other Series'") == 1


def test_colliding_names_warn_and_keep_first(tmp_path, capsys):
    write_json(tmp_path, {"Some Series": SOME_SERIES, "Some series!": {"writer": "Other Writer"}})
    metadata = SeriesMetadata(str(tmp_path))
    assert metadata.get("Some Series")["writer"] == "Some Writer"
    assert "ignoring it" in capsys.readouterr().out


@pytest.mark.parametrize("content", ["{not json", "[]", '{"Series": "text"}', '{"Series": {"writer": 3}}'])
def test_malformed_json_fails(tmp_path, content):
    (tmp_path / FILE_NAME).write_text(content, encoding="utf-8")
    with pytest.raises(ValueError):
        SeriesMetadata(str(tmp_path))


def test_field_option_wins_over_json(tmp_path):
    write_json(tmp_path, {"Some Series": SOME_SERIES})
    command = Command(str(tmp_path), is_manga=True, publisher="Other Publisher")
    comic = command.build_comic("Some Series v11.zip", SeriesMetadata(str(tmp_path)))
    assert comic.publisher == "Other Publisher"
    assert comic.writer == "Some Writer"
    assert comic.volume == 11


def test_writer_element_order_and_skips_none():
    comic = Comic(series="Some Series", volume=11, number=3, writer="Some Writer", publisher="Some Publisher",
                  genre="Genre A", language_iso="xx", is_manga=True)
    root = ComicInfoWriter(comic, directory_path=None).build()
    assert [element.tag for element in root] == [
        "Title", "Series", "Number", "Volume", "Writer", "Publisher", "Genre", "LanguageISO", "Manga",
    ]
