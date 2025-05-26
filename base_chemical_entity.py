from __future__ import annotations
import threading
from typing import ClassVar, Self, TypeVar, Generic, final, Iterable, Mapping
from abc import ABC, abstractmethod

TData = TypeVar("TData")
TKey = TypeVar("TKey")


@final
class BaseChemicalEntity(ABC, Generic[TData, TKey]):
    """
    Base class for chemical entities with a registry system.

    This class provides a centralized registry for managing instances of chemical
    entities, ensuring uniqueness and thread safety.

    Attributes:
        registry (ClassVar[list[Self] | None]): List of all registered instances.
        key_dictionary (ClassVar[dict[TKey, int] | None]): Mapping from keys to registry indices.
        _lock (ClassVar[threading.Lock]): Thread lock for registry modifications.
        index (int): Index of the instance in the registry.
        data (TData): Data associated with the instance.
        symbol (str): Display symbol of the instance.
        keys (tuple[TKey]): Keys for the instance.
    """

    registry: ClassVar[list[Self] | None] = None
    key_dictionary: ClassVar[dict[TKey, int] | None] = None
    _lock: ClassVar[threading.RLock] = threading.RLock()

    index: int
    data: TData
    symbol: str
    keys: tuple[TKey]

    def __new__(
        cls, identifier: int | TKey | None = None, data: TData | None = None
    ) -> Self:
        """
        Get an existing instance or create a new one.

        Args:
            identifier (int | TKey | None): Existing ID or key for lookup.
            data (TData | None): Data for new instance creation.

        Returns:
            Self: Retrieved or newly created instance.

        Raises:
            ValueError: Missing identifier/data or key conflict.
            IndexError: Invalid integer identifier.
            TypeError: Unsupported identifier type.
        """
        if cls.registry is None:
            cls.registry = []
        if cls.key_dictionary is None:
            cls.key_dictionary = {}

        match (identifier, data):
            case (None, None):
                raise ValueError("Must provide identifier or data")
            case (int() as i, None) if 0 <= i < len(cls.registry):
                return cls.registry[i]
            case (int(), None):
                raise IndexError(f"Invalid index: {identifier}")
            case (_, None) if identifier in cls.key_dictionary:  # type: ignore
                return cls.registry[cls.key_dictionary[identifier]]  # type: ignore
            case (_, None):
                raise TypeError(f"Invalid identifier type: {type(identifier)}")
            case _:
                with cls._lock:
                    instance = super().__new__(cls)
                    instance._init(len(cls.registry), data)  # type: ignore

                    keys = instance.generate_key()
                    for key in keys:
                        if key in cls.key_dictionary:
                            raise ValueError(f"Key conflict: {key}")

                    cls.registry.append(instance)
                    for key in keys:
                        cls.key_dictionary[key] = instance.index
                    return instance

    @abstractmethod
    def generate_key(self) -> tuple[TKey]:
        """
        Generate registry keys for the instance.

        Returns:
            tuple[TKey]: Registry keys.
        """
        ...

    def _init(self, index: int, data: TData) -> None:
        """
        Initialize the instance attributes.

        Args:
            index (int): Index of the instance in the registry.
            data (TData): Data for the instance.
        """
        self.index = index
        self.data = data

    def __repr__(self) -> str:
        """
        Return the official string representation of the instance.

        Returns:
            str: Display symbol of the instance.
        """
        return self.symbol

    @classmethod
    def extend_data(cls, data_list: Iterable[TData]) -> None:
        """
        Extend the registry with new instances from an iterable of data objects.

        Args:
            data_iterable (Iterable[TData]): Iterable of data objects to create instances from.
        """
        for data in data_list:
            cls(data=data)
    @classmethod
    def clear_data(cls) -> None:
        """
        Clear the registry and key dictionary, resetting them to None.
        """
        with cls._lock:
            cls.registry = None
            cls.key_dictionary = None
            
    @classmethod
    def load_data(cls, data_list: Iterable[TData]) -> None:
        """
        Load multiple instances from an iterable of data objects.

        Args:
            data_iterable (Iterable[TData]): Iterable of data objects to create instances from.
        """
        cls.clear_data()
        cls.extend_data(data_list)
