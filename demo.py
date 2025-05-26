from element import Element, ElementData
from valence_element import ValenceElement, ValenceElementData
from atomic_group import AtomicGroup, AtomicGroupData, NO_VALENCE
from element_table import load_simple_elements

load_simple_elements()

_elements = ((ValenceElement("C(+4)"), 1), (ValenceElement("O(-2)"), 3))
AtomicGroup(data=AtomicGroupData(_elements))
_elements = ((ValenceElement("C(-4)"), 1), (ValenceElement("H(+1)"), 4))

AtomicGroup(data=AtomicGroupData(_elements, NO_VALENCE, symbol="-Me"))
print(AtomicGroup.registry)
print([a.base_symbol for a in AtomicGroup.registry])
