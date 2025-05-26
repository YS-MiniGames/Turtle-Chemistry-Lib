from element import Element, ElementData
from valence_element import ValenceElement, ValenceElementData


# List of simple elements
def SIMPLE_ELEMENTS():
    return [
        ElementData("H", 1),
        ElementData("He", 4),
        ElementData("C", 12),
        ElementData("N", 14),
        ElementData("O", 16),
        ElementData("Na", 23),
        ElementData("Mg", 24),
        ElementData("Al", 27),
        ElementData("P", 31),
        ElementData("S", 32),
        ElementData("Cl", 35.5),
        ElementData("K", 39),
        ElementData("Ca", 40),
        ElementData("Fe", 56),
        ElementData("Cu", 64),
        ElementData("Zn", 65),
        ElementData("Ag", 108),
        ElementData("Ba", 137),
        ElementData("Au", 197),
        ElementData("Hg", 201),
    ]


# List of valence elements
def SIMPLE_VALENCE_ELEMENTS():
    return [
        # Zero-valence elements
        ValenceElementData(Element("H"), 0),
        ValenceElementData(Element("He"), 0),
        ValenceElementData(Element("C"), 0),
        ValenceElementData(Element("N"), 0),
        ValenceElementData(Element("O"), 0),
        ValenceElementData(Element("Mg"), 0),
        ValenceElementData(Element("Al"), 0),
        ValenceElementData(Element("P"), 0),
        ValenceElementData(Element("S"), 0),
        ValenceElementData(Element("Cl"), 0),
        ValenceElementData(Element("Fe"), 0),
        ValenceElementData(Element("Cu"), 0),
        ValenceElementData(Element("Zn"), 0),
        ValenceElementData(Element("Ag"), 0),
        ValenceElementData(Element("Ba"), 0),
        ValenceElementData(Element("Au"), 0),
        ValenceElementData(Element("Hg"), 0),
        # Valence elements
        ValenceElementData(Element("H"), +1),
        ValenceElementData(Element("C"), +2),
        ValenceElementData(Element("C"), +4),
        ValenceElementData(Element("C"), -4),
        ValenceElementData(Element("N"), -3),
        ValenceElementData(Element("N"), +5),
        ValenceElementData(Element("O"), -2),
        ValenceElementData(Element("Na"), +1),
        ValenceElementData(Element("Mg"), +2),
        ValenceElementData(Element("Al"), +3),
        ValenceElementData(Element("P"), +5),
        ValenceElementData(Element("S"), +4),
        ValenceElementData(Element("S"), +6),
        ValenceElementData(Element("Cl"), -1),
        ValenceElementData(Element("K"), +1),
        ValenceElementData(Element("Ca"), +2),
        ValenceElementData(Element("Fe"), +2),
        ValenceElementData(Element("Fe"), +3),
        ValenceElementData(Element("Cu"), +1),
        ValenceElementData(Element("Cu"), +2),
        ValenceElementData(Element("Zn"), +2),
        ValenceElementData(Element("Ag"), +1),
        ValenceElementData(Element("Ba"), +2),
        ValenceElementData(Element("Hg"), +2),
    ]


def load_simple_elements():
    Element.load_data(SIMPLE_ELEMENTS())
    ValenceElement.load_data(SIMPLE_VALENCE_ELEMENTS())
