import xml.etree.ElementTree as ET


# in-place prettyprint formatter
def indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for child in elem:
            indent(child, level + 1)
        if not child.tail or not child.tail.strip():
            child.tail = i
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


if __name__ == "__main__":
    # list with examples
    testlist = [["VAN GOGH", "Sternennacht", "Impressionismus"],["PICASSO", "Dora Maar", "Kubismus"],
            ["ALBRECHT DUERER", "Betende Haende", "Renaissance"]]

    root = ET.Element("aiml", version="1.0.1", encoding="UTF-8")

    for entry in testlist:
        category = ET.SubElement(root, "category")

        ET.SubElement(category, "pattern").text = "XCHECKART " + entry[0].upper()

        template = ET.SubElement(category, "template")

        think = ET.SubElement(template, "think")

        ET.SubElement(think, "set", name="bild").text = entry[1]
        ET.SubElement(think, "set", name="epoche").text = entry[2]

    indent(root)
    tree = ET.ElementTree(root)
    tree.write("artists.aiml")
