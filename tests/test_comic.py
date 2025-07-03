import os
import sys

from src.lib.comic import Comic

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_from_file_name_basic():
    file_name = "Some Series v01 [Some Book].zip"
    comic = Comic.from_file_name(file_name)
    assert comic is not None
    assert comic.series == "Some Series"
    assert comic.volume == "01"
    assert comic.number is None
    assert comic.title == "Some Book"
    assert comic.is_manga is False
    assert comic.file_name == file_name


def test_from_file_name_no_title():
    comic = Comic.from_file_name("Some Series v3.zip")
    assert comic.series == "Some Series"
    assert comic.volume == "3"
    assert comic.title is None


def test_from_file_name_series_only():
    comic = Comic.from_file_name("Some Series.zip")
    assert comic.series == "Some Series"
    assert comic.volume is None
    assert comic.title is None

def test_from_file_name_with_number():
    comic = Comic.from_file_name("Some Series #88 [Some Book].zip")
    assert comic.number == "88"
    assert comic.volume is None


def test_from_file_name_manga():
    comic = Comic.from_file_name("Some Manga v45 [Another Book].zip", is_manga=True)
    assert comic.is_manga is True


def test_from_file_name_invalid():
    comic = Comic.from_file_name("invalid_filename.txt")
    assert comic is None
