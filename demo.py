from element import Element,ElementData
from valence_element import ValenceElement,ValenceElementData
from atomic_group import AtomicGroup,AtomicGroupData,NO_VALENCE

Element(data=ElementData("O",16))
print(Element("O"))
print(Element("O").data.atomic_weight)
a=Element("O")
b=Element("O")
print(a is b)

Element(data=ElementData("C",12))
Element(data=ElementData("H",1))

ValenceElement(data=ValenceElementData(Element("C"),+4))
ValenceElement(data=ValenceElementData(Element("C"),-4))
ValenceElement(data=ValenceElementData(Element("O"),-2))
ValenceElement(data=ValenceElementData(Element("H"),+1))
print(ValenceElement.registry)

_elements=((ValenceElement("C(+4)"),1),(ValenceElement("O(-2)"),3))
AtomicGroup(data=AtomicGroupData(_elements))
_elements=((ValenceElement("C(-4)"),1),(ValenceElement("H(+1)"),4))

AtomicGroup(data=AtomicGroupData(_elements,NO_VALENCE,symbol="-Me"))
print(AtomicGroup.registry)
print([a.base_symbol for a in AtomicGroup.registry])