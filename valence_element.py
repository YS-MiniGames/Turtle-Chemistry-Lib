from __future__ import annotations
from dataclasses import dataclass
from element import Element
from base_chemical_entity import BaseChemicalEntity


@dataclass(frozen=True)
class ValenceElementData:
    """Valence-specific element data container.

    Attributes:
        element: Base element reference
        valence: Oxidation state value
        symbol: Optional custom symbol
    """

    base_element: Element
    valence: int
    symbol: str | None = None


class ValenceElement(
    BaseChemicalEntity[ValenceElementData, tuple[str, tuple[Element, int]]]
):
    """Element with specific oxidation state representation.

    Attributes:
        base_element: Reference to base element
        valence: Oxidation state value
    """

    base_element: Element
    base_symbol: str
    valence: int

    def generate_key(self):
        """Generate registry keys as per base entity requirements."""
        return (self.symbol, (self.base_element, self.valence))

    def generate_symbol(self) -> str:
        """Generate formatted symbol with valence notation."""
        return self.data.symbol or f"{self.base_element.symbol}({self.valence:+})"

    def _init(self, index: int, data: ValenceElementData) -> None:
        """Initialize instance attributes."""
        super()._init(index, data)
        self.base_element = data.base_element
        self.base_symbol = self.base_element.symbol
        self.valence = data.valence
        self.symbol = self.generate_symbol()
