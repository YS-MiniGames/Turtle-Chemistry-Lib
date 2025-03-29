from __future__ import annotations
import threading
from typing import ClassVar, Self, TypeVar, Generic, final
from abc import ABC, abstractmethod

TData = TypeVar("TData")
TKey = TypeVar("TKey")


@final
class BaseChemicalEntity(ABC, Generic[TData, TKey]):
    """Chemical entity base class with registry system.

    Attributes:
        registry: ClassVar list storing all registered instances
        key_dictionary: ClassVar mapping from keys to registry indices
        _lock: Thread lock for registry modifications
    """

    registry: ClassVar[list[Self] | None] = None
    key_dictionary: ClassVar[dict[TKey, int] | None] = None
    _lock: ClassVar[threading.Lock] = threading.Lock()

    index: int
    data: TData
    symbol: str
    keys: tuple[TKey]

    def __new__(
        cls, identifier: int | TKey | None = None, data: TData | None = None
    ) -> Self:
        """Get existing or create new instance.

        Args:
            identifier: Existing ID or key for lookup
            data: Data for new instance creation

        Returns:
            Retrieved or newly created instance

        Raises:
            ValueError: Missing identifier/data or key conflict
            IndexError: Invalid integer identifier
            TypeError: Unsupported identifier type
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
    def generate_key(self) -> tuple[TKey]: ...

    def _init(self, index: int, data: TData) -> None:
        self.index = index
        self.data = data

    def __repr__(self) -> str:
        return self.symbol
