from __future__ import annotations
from dataclasses import dataclass
from base_chemical_entity import BaseChemicalEntity


@dataclass(frozen=True)
class ElementData:
    """
    Data container for Element.

    Attributes:
        symbol (str | None): Element symbol (e.g., 'H'). Defaults to None.
        atomic_weight (float | None): Average atomic weight in g/mol. Defaults to None.
    """
    symbol: str | None = None
    atomic_weight: float | None = None


class Element(BaseChemicalEntity[ElementData, str]):
    """
    Represents a fundamental chemical element with registry support.

    This class extends BaseChemicalEntity and provides methods to generate
    the display symbol of the element.

    Attributes:
        symbol (str): Short element symbol.
        atomic_weight (float | None): Average atomic mass value.
    """

    def generate_key(self) -> tuple[str]:
        """
        Generate registry key for the element.

        Returns:
            tuple[str]: Registry key.
        """
        return (self.symbol,)

    def generate_symbol(self) -> str:
        """
        Generate the display symbol of the element.

        Returns:
            str: Display symbol.
        """
        return self.data.symbol or f"<Element#{self.index}>"

    def _init(self, index: int, data: ElementData) -> None:
        """
        Initialize the element instance.

        Args:
            index (int): Index of the instance in the registry.
            data (ElementData): Data for the element.
        """
        super()._init(index, data)
        self.symbol = self.generate_symbol()