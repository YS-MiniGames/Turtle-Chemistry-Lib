from __future__ import annotations
from dataclasses import dataclass
from typing import final
from element import Element
from valence_element import ValenceElement
from base_chemical_entity import BaseChemicalEntity

type GroupComponent = Element | ValenceElement | AtomicGroup
type GroupElements = tuple[tuple[GroupComponent, int]]


NO_VALENCE = "NO_VALENCE"


@dataclass(frozen=True)
class AtomicGroupData:
    elements: GroupElements
    valence: int | None = None
    base_symbol: str | None = None
    symbol: str | None = None
    elements_key: bool = True


@final
class AtomicGroup(BaseChemicalEntity[AtomicGroupData, tuple[str]]):
    """Atomic group with valence calculation capabilities.

    Attributes:
        composition: Component elements with counts
        valence: Calculated total valence
        symbol_without_valence: Base group symbol
    """

    elements: GroupElements
    valence: int | None
    base_symbol: str

    def generate_key(self):
        """Generate registry keys from component tuple."""
        if self.data.elements_key:
            return (self.symbol, self.elements)
        return (self.symbol,)

    def generate_valence(self) -> int | None:
        if self.data.valence == NO_VALENCE:
            return None
        if self.data.valence is not None:
            return self.data.valence
        total = 0
        for item in self.elements:
            match item:
                case (ValenceElement(valence=v), count) | (
                    AtomicGroup(valence=v),
                    count,
                ):
                    total += v * count
                case _:
                    return None
        return total

    def generate_base_symbol(self) -> str:
        if self.data.base_symbol:
            return self.data.base_symbol
        li = []
        for item in self.elements:
            match item:
                case (Element() as e, 1):
                    li.append(e.symbol)
                case (ValenceElement() as e, 1) | (AtomicGroup() as e, 1):
                    li.append(e.base_symbol)
                case (Element() as e, count):
                    li.append(e.symbol)
                    li.append(str(count))
                case (ValenceElement() as e, count) | (AtomicGroup() as e, count):
                    li.append(e.base_symbol)
                    li.append(str(count))
                case _:
                    raise ValueError("Wrong Elements")
        return "".join(li)

    def generate_symbol(self) -> str:
        if self.data.symbol:
            return self.data.symbol
        if self.valence is None:
            return f"-{self.base_symbol}"
        return f"-{self.base_symbol}({self.valence:+})"

    def _init(self, index: int, data: AtomicGroupData) -> None:
        super()._init(index, data)
        self.elements = self.data.elements
        self.valence = self.generate_valence()
        self.base_symbol = self.generate_base_symbol()
        self.symbol = self.generate_symbol()
