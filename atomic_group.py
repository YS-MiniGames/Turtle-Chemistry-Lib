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
    """
    Data container for AtomicGroup.

    Attributes:
        elements (GroupElements): Composition of elements and their counts.
        valence (int | None): Total valence of the group. Defaults to None.
        base_symbol (str | None): Base symbol of the group. Defaults to None.
        symbol (str | None): Display symbol of the group. Defaults to None.
        elements_key (bool): Whether to use elements as part of the key. Defaults to True.
    """
    elements: GroupElements
    valence: int | None = None
    base_symbol: str | None = None
    symbol: str | None = None
    elements_key: bool = True


@final
class AtomicGroup(BaseChemicalEntity[AtomicGroupData, tuple[str]]):
    """
    Represents an atomic group with valence calculation capabilities.

    This class extends BaseChemicalEntity and provides methods to calculate
    the total valence of the group and generate symbols based on its composition.

    Attributes:
        elements (GroupElements): Composition of elements and their counts.
        valence (int | None): Calculated total valence of the group.
        base_symbol (str): Base symbol of the group.
        symbol (str): Display symbol of the group.
    """

    def generate_key(self) -> tuple[str]:
        """
        Generate registry keys from component tuple.

        Returns:
            tuple[str]: Registry keys.
        """
        if self.data.elements_key:
            return (self.symbol, self.elements)
        return (self.symbol,)

    def generate_valence(self) -> int | None:
        """
        Calculate the total valence of the atomic group.

        The valence is calculated based on the valence of each component element
        and their respective counts.

        Returns:
            int | None: Total valence of the group, or None if calculation is not possible.
        """
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
        """
        Generate the base symbol of the atomic group.

        The base symbol is constructed from the symbols of the component elements
        and their counts.

        Returns:
            str: Base symbol of the group.
        """
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
        """
        Generate the display symbol of the atomic group.

        The display symbol includes the base symbol and the valence (if applicable).

        Returns:
            str: Display symbol of the group.
        """
        if self.data.symbol:
            return self.data.symbol
        if self.valence is None:
            return f"-{self.base_symbol}"
        return f"-{self.base_symbol}({self.valence:+})"

    def _init(self, index: int, data: AtomicGroupData) -> None:
        """
        Initialize the atomic group instance.

        Args:
            index (int): Index of the instance in the registry.
            data (AtomicGroupData): Data for the atomic group.
        """
        super()._init(index, data)
        self.elements = self.data.elements
        self.valence = self.generate_valence()
        self.base_symbol = self.generate_base_symbol()
        self.symbol = self.generate_symbol()