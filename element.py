from __future__ import annotations
from dataclasses import dataclass
from base_chemical_entity import BaseChemicalEntity


@dataclass(frozen=True)
class ElementData:
    """Chemical element metadata container.

    Attributes:
        symbol: Element symbol (e.g. 'H')
        atomic_weight: Average atomic weight in g/mol
    """

    symbol: str | None = None
    atomic_weight: float | None = None


class Element(BaseChemicalEntity[ElementData, str]):
    """Fundamental chemical element with registry support.

    Attributes:
        symbol: Short element symbol
        atomic_weight: Average atomic mass value
    """

    def generate_key(self):
        return (self.symbol,)

    def generate_symbol(self) -> str:
        """Generate display symbol using data or fallback format."""
        return self.data.symbol or f"<Element#{self.index}>"

    def _init(self, index: int, data: ElementData) -> None:
        """Initialize instance attributes."""
        super()._init(index, data)
        self.symbol = self.generate_symbol()
