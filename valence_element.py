from __future__ import annotations
from dataclasses import dataclass
from element import Element
from base_chemical_entity import BaseChemicalEntity


@dataclass(frozen=True)
class ValenceElementData:
    """
    Data container for ValenceElement.

    Attributes:
        base_element (Element): Reference to the base element.
        valence (int): Oxidation state value.
        symbol (str | None): Optional custom symbol. Defaults to None.
    """
    base_element: Element
    valence: int
    symbol: str | None = None


class ValenceElement(
    BaseChemicalEntity[ValenceElementData, tuple[str, tuple[Element, int]]]
):
    """
    Represents an element with a specific oxidation state.

    This class extends BaseChemicalEntity and provides methods to generate
    the display symbol of the valence element.

    Attributes:
        base_element (Element): Reference to the base element.
        base_symbol (str): Symbol of the base element.
        valence (int): Oxidation state value.
        symbol (str): Display symbol of the valence element.
    """

    def generate_key(self) -> tuple[str, tuple[Element, int]]:
        """
        Generate registry keys for the valence element.

        Returns:
            tuple[str, tuple[Element, int]]: Registry keys.
        """
        return (self.symbol, (self.base_element, self.valence))

    def generate_symbol(self) -> str:
        """
        Generate the display symbol of the valence element.

        Returns:
            str: Display symbol.
        """
        return self.data.symbol or f"{self.base_element.symbol}({self.valence:+})"

    def _init(self, index: int, data: ValenceElementData) -> None:
        """
        Initialize the valence element instance.

        Args:
            index (int): Index of the instance in the registry.
            data (ValenceElementData): Data for the valence element.
        """
        super()._init(index, data)
        self.base_element = data.base_element
        self.base_symbol = self.base_element.symbol
        self.valence = data.valence
        self.symbol = self.generate_symbol()