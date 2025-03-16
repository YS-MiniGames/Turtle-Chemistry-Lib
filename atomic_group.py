from __future__ import annotations
import threading
from dataclasses import dataclass
from typing import ClassVar
from element import Element
from valence_element import ValenceElement

type AtomicGroupElementsType = tuple[
    Element | ValenceElement | tuple[Element | ValenceElement, int]
]


@dataclass(frozen=True)
class AtomicGroupData:
    """原子基团的基础数据类"""

    elements: AtomicGroupElementsType
    valence: int | None = None
    name: str | None = None
    symbol_without_valence: str | None = None
    symbol: str | None = None


class AtomicGroup:
    """表示原子基团的类，实现单例注册管理

    类属性：
        registry: 所有实例的注册表
        symbol_dictionary: 符号到索引的映射
        composition_dictionary: (元素组合,价态)到索引的映射
        _lock: 线程安全锁

    实例属性：
        index: 注册表索引
        data: 完整基团数据
        symbol: 基团符号表示
        composition: 不可变的元素组合元组
        valence: 基团整体价态
    """

    registry: ClassVar[list[AtomicGroup]] = []
    symbol_dictionary: ClassVar[dict[str, int]] = {}
    composition_dictionary: ClassVar[dict[AtomicGroupElementsType, int]] = {}
    _lock: ClassVar[threading.Lock] = threading.Lock()

    index: int
    data: AtomicGroupData
    composition: AtomicGroupElementsType
    valence: int | None
    symbol: str
    symbol_without_valence: str

    def __new__(
        cls,
        identifier: int | str | AtomicGroupElementsType | None = None,
        data: AtomicGroupData | None = None,
    ) -> AtomicGroup:
        """通过标识符获取或创建新实例"""
        if data is None:
            if identifier is None:
                raise ValueError("必须提供标识符（索引/符号/组合）")

            if isinstance(identifier, int):
                if not 0 <= identifier < len(cls.registry):
                    raise IndexError(
                        f"基团索引越界: {identifier} (范围 0-{len(cls.registry)-1})"
                    )
                return cls.registry[identifier]

            if isinstance(identifier, str):
                if identifier not in cls.symbol_dictionary:
                    raise KeyError(f"基团符号不存在: '{identifier}'")
                return cls.registry[cls.symbol_dictionary[identifier]]

            if isinstance(identifier, tuple):
                if identifier not in cls.composition_dictionary:
                    raise KeyError(f"基团组合不存在: {identifier}")
                return cls.registry[cls.composition_dictionary[identifier]]

            raise TypeError("标识符应为int/str/组合")

        # 创建新实例
        with cls._lock:
            new_index = len(cls.registry)
            instance = super().__new__(cls)
            instance._init(new_index, data)

            # 检查符号冲突
            if instance.symbol in cls.symbol_dictionary:
                existing = cls.symbol_dictionary[instance.symbol]
                raise ValueError(f"符号冲突: {instance.symbol} 已用于索引 {existing}")

            # 注册实例
            cls.registry.append(instance)
            cls.symbol_dictionary[instance.symbol] = new_index
            return instance

    def generate_valence(self) -> int | None:
        if self.data.valence is not None:
            return self.data.valence

        valence = 0
        for composition in self.data.elements:
            if isinstance(composition, Element):
                return None
            elif isinstance(composition, ValenceElement):
                valence += composition.valence
            elif isinstance(composition, tuple):
                element = composition[0]
                count = composition[1]
                if isinstance(element, Element):
                    return None
                elif isinstance(element, ValenceElement):
                    valence += element.valence * count
                else:
                    raise ValueError("基团元素数据错误")
            else:
                raise ValueError("基团元素数据错误")
        return valence

    def generate_symbol_without_valence(self) -> str:
        """生成基团符号表示"""
        if self.data.symbol_without_valence:
            return self.data.symbol_without_valence

        symbol_list = []
        for composition in self.data.elements:
            if isinstance(composition, Element):
                symbol_list.append(composition.symbol)
            elif isinstance(composition, ValenceElement):
                symbol_list.append(composition.element.symbol)
            elif isinstance(composition, tuple):
                element = composition[0]
                count = composition[1]
                if isinstance(element, Element):
                    symbol_list.append(element.symbol)
                elif isinstance(element, ValenceElement):
                    symbol_list.append(element.element.symbol)
                else:
                    raise ValueError("基团元素数据错误")
                if count > 1:
                    symbol_list.append(str(count))
            else:
                raise ValueError("基团元素数据错误")
        new_symbol = "".join(symbol_list)
        return new_symbol

    def generate_symbol(self) -> str:
        if self.data.symbol:
            return self.data.symbol
        if self.valence is not None:
            return f"{self.symbol_without_valence}({self.valence:+})"
        return self.symbol_without_valence

    def _init(self, index: int, data: AtomicGroupData) -> None:
        """初始化实例属性"""
        self.index = index
        self.data = data
        self.composition = data.elements
        self.valence = self.generate_valence()
        self.symbol_without_valence = self.generate_symbol_without_valence()
        self.symbol = self.generate_symbol()

    def __repr__(self) -> str:
        return self.symbol

    @classmethod
    def new_atomic_group(cls, data: AtomicGroupData) -> AtomicGroup:
        """创建新基团的工厂方法"""
        return cls(None, data)  # type: ignore

    @classmethod
    def extend_data(cls, data_list: list[AtomicGroupData]) -> list[AtomicGroup]:
        """批量创建基团实例"""
        return [cls.new_atomic_group(data) for data in data_list]

    @classmethod
    def clear_data(cls) -> None:
        """清空所有注册数据"""
        with cls._lock:
            cls.registry.clear()
            cls.symbol_dictionary.clear()
            cls.composition_dictionary.clear()


if __name__ == "__main__":
    # 测试用例
    from element_table import SIMPLE_ELEMENTS
    from valence_element import ValenceElement, ValenceElementData

    Element.extend_data(SIMPLE_ELEMENTS)
    ValenceElement.extend_data(
        [
            ValenceElementData(Element("O"), -2),
            ValenceElementData(Element("H"), +1),
            ValenceElementData(Element("C"), +4),
        ]
    )

    VH = ValenceElement("H(+1)")
    VO = ValenceElement("O(-2)")
    VC = ValenceElement("C(+4)")
    print(VH, VO, VH.composition)

    OH = AtomicGroup.new_atomic_group(AtomicGroupData((VO, VH), name="Hydroxide"))
    CO3 = AtomicGroup.new_atomic_group(AtomicGroupData((VC,(VO,3)), name="Carbonate"))
    
    print(CO3)