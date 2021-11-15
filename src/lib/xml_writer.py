import os
from xml.dom import minidom
from xml.etree import cElementTree as elementTree


def write_xml(xml_element, directory_path):
    file_path = os.path.join(directory_path, "ComicInfo.xml")
    parsed_xml = minidom.parseString(elementTree.tostring(xml_element, encoding="utf-8"))
    pretty_xml = parsed_xml.toprettyxml(indent="  ", encoding="utf-8")
    with open(file_path, "wb") as file:
        file.write(pretty_xml)
    return file_path
