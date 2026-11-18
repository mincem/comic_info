import xml.etree.ElementTree as elementTree

from .xml_writer import write_xml

# Optional elements and their Comic attribute, in the order ComicInfo.xsd requires (it's an xs:sequence)
OPTIONAL_FIELDS = (
    ("Number", "number"),
    ("Volume", "volume"),
    ("Writer", "writer"),
    ("Penciller", "penciller"),
    ("Publisher", "publisher"),
    ("Imprint", "imprint"),
    ("Genre", "genre"),
    ("LanguageISO", "language_iso"),
)


class ComicInfoWriter:
    def __init__(self, comic, directory_path):
        self.comic = comic
        self.directory_path = directory_path

    def write(self):
        return write_xml(xml_element=self.build(), directory_path=self.directory_path)

    def build(self):
        root = elementTree.Element("ComicInfo")
        elementTree.SubElement(root, "Title").text = self.comic.title
        elementTree.SubElement(root, "Series").text = self.comic.series
        for element_name, attribute in OPTIONAL_FIELDS:
            value = getattr(self.comic, attribute)
            if value is not None:
                elementTree.SubElement(root, element_name).text = str(value)
        elementTree.SubElement(root, "Manga").text = self.manga_field_value()
        return root

    def manga_field_value(self):
        return "YesAndRightToLeft" if self.comic.is_manga else "No"
