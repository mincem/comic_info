import xml.etree.ElementTree as elementTree

from .xml_writer import write_xml


class ComicInfoWriter:
    def __init__(self, comic, directory_path):
        self.comic = comic
        self.directory_path = directory_path

    def write(self):
        root = elementTree.Element("ComicInfo")
        elementTree.SubElement(root, "Title").text = self.comic.title
        elementTree.SubElement(root, "Series").text = self.comic.series
        if self.comic.volume is not None:
            elementTree.SubElement(root, "Volume").text = str(self.comic.volume)
        if self.comic.number is not None:
            elementTree.SubElement(root, "Number").text = str(self.comic.number)
        if self.comic.publisher is not None:
            elementTree.SubElement(root, "Publisher").text = self.comic.publisher
        elementTree.SubElement(root, "Manga").text = self.manga_field_value()

        return write_xml(xml_element=root, directory_path=self.directory_path)

    def manga_field_value(self):
        return "YesAndRightToLeft" if self.comic.is_manga else "No"
