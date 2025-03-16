from __future__ import annotations
import threading
from dataclasses import dataclass
from typing import ClassVar
from element import Element


@dataclass(frozen=True)
class ValenceElementData:
    """带价态元素的不可变数据容器类

    Attributes:
        element (Element): 基础元素对象
        valence (int): 元素的氧化态/价态
        symbol (str | None): 可选的自定义符号表示（如"Fe+3"）
        name (str | None): 可选的全名（如"Iron(III)"）
    """

    element: Element
    valence: int
    symbol: str | None = None
    name: str | None = None


class ValenceElement:
    """表示带特定价态元素的类，提供注册管理机制

    实现线程安全的价态元素实例创建和访问，支持通过多种标识符类型获取实例。
    维护全局注册表记录所有创建的实例。

    Class Attributes:
        registry (ClassVar[list[ValenceElement]]): 所有实例的注册表
        symbol_dictionary (ClassVar[dict[str, int]]): 符号到注册索引的映射
        element_valence_dictionary (ClassVar[dict[tuple[Element, int], int]]): (元素,价态)到索引的映射
        _lock (ClassVar[threading.Lock]): 线程安全锁

    Instance Attributes:
        index (int): 在注册表中的唯一索引
        data (ValenceElementData): 完整价态元素数据
        element (Element): 关联的基础元素
        valence (int): 元素的氧化态
        symbol (str): 包含价态的符号表示
    """

    registry: ClassVar[list[ValenceElement]] = []
    symbol_dictionary: ClassVar[dict[str, int]] = {}
    composition_dictionary: ClassVar[dict[tuple[Element, int], int]] = {}
    _lock: ClassVar[threading.Lock] = threading.Lock()

    index: int
    data: ValenceElementData
    element: Element
    valence: int
    composition: tuple[Element, int]
    symbol: str

    def __new__(
        cls,
        identifier: int | str | tuple[Element, int] | None = None,
        data: ValenceElementData | None = None,
    ) -> ValenceElement:
        """通过多种标识符类型获取或创建实例

        Args:
            identifier: 标识符类型可以是：
                - int: 直接使用注册表索引
                - str: 符号表示（如"Fe(+2)"）
                - tuple: (元素, 价态)组合
                - None: 当需要创建新实例时需配合data参数使用
            data: 用于创建新实例的数据对象

        Returns:
            ValenceElement: 已存在的或新创建的实例

        Raises:
            ValueError: 无效标识符或重复条目时引发
            IndexError: 注册表索引越界时引发
            KeyError: 符号或元素价态组合不存在时引发
            TypeError: 标识符类型无效时引发
        """
        if data is None:
            if identifier is None:
                raise ValueError(
                    "必须提供标识符（整数索引、符号或(Element, valence)元组）"
                )

            if isinstance(identifier, int):
                if not 0 <= identifier < len(cls.registry):
                    raise IndexError(
                        f"价态元素索引越界: {identifier} (有效范围 0-{len(cls.registry)-1})"
                    )
                return cls.registry[identifier]

            if isinstance(identifier, str):
                if identifier not in cls.symbol_dictionary:
                    raise KeyError(f"价态元素符号不存在: '{identifier}'")
                return cls.registry[cls.symbol_dictionary[identifier]]

            if isinstance(identifier, tuple):
                if identifier not in cls.composition_dictionary:
                    raise KeyError(f"价态组合不存在: '{identifier}'")
                return cls.registry[cls.composition_dictionary[identifier]]

            raise TypeError("无效标识符类型，应为int/str/tuple[Element, int]")

        # 创建新实例
        with cls._lock:
            new_index = len(cls.registry)
            instance = super().__new__(cls)
            instance._init(new_index, data)

            if instance.symbol in cls.symbol_dictionary:
                existing_index = cls.symbol_dictionary[instance.symbol]
                raise ValueError(
                    f"符号冲突: {instance.symbol}，已用于索引 {existing_index}"
                )

            if instance.composition in cls.composition_dictionary:
                existing_index = cls.composition_dictionary[instance.composition]
                raise ValueError(
                    f"价态重复: {instance.symbol}，已用于索引 {existing_index}"
                )

            cls.registry.append(instance)
            cls.symbol_dictionary[instance.symbol] = new_index
            cls.composition_dictionary[(instance.element, instance.valence)] = new_index
            return instance

    def generate_symbol(self) -> str:
        """生成标准的带价态符号表示

        Returns:
            str: 如果未提供自定义符号，返回格式为"SYM(+VAL)"的字符串；
                 否则直接返回自定义符号
        """
        return (
            self.data.symbol
            if self.data.symbol
            else f"{self.element.symbol}({self.valence:+})"
        )

    def _init(self, index: int, data: ValenceElementData) -> None:
        """初始化实例属性

        Args:
            index (int): 分配的注册表索引
            data (ValenceElementData): 要存储的价态元素数据
        """
        self.index = index
        self.data = data
        self.element = data.element
        self.valence = data.valence
        self.composition = (self.element, self.valence)
        self.symbol = self.generate_symbol()

    def __repr__(self) -> str:
        """返回符号表示用于调试和显示"""
        return self.symbol

    @classmethod
    def new_valence_element(cls, data: ValenceElementData) -> ValenceElement:
        """创建新价态元素的工厂方法

        Args:
            data (ValenceElementData): 完整的价态元素数据

        Returns:
            ValenceElement: 新创建的实例
        """
        return cls(None, data)  # type: ignore

    @classmethod
    def extend_data(cls, data_list: list[ValenceElementData]) -> list[ValenceElement]:
        """批量创建价态元素实例

        Args:
            data_list (list[ValenceElementData]): 价态元素数据对象列表

        Returns:
            list[ValenceElement]: 创建的实例列表
        """
        return [cls.new_valence_element(data) for data in data_list]

    @classmethod
    def clear_data(cls) -> None:
        """清空所有注册数据，重置类到初始状态"""
        with cls._lock:
            cls.registry.clear()
            cls.symbol_dictionary.clear()
            cls.composition_dictionary.clear()


if __name__ == "__main__":
    # 测试基础元素
    from element_table import SIMPLE_ELEMENTS

    Element.extend_data(SIMPLE_ELEMENTS)

    # 测试价态元素
    V = [
        ValenceElementData(Element("Fe"), 2, None, "Iron(II)"),
        ValenceElementData(Element("Fe"), 3, "Fe+3", "Iron(III)"),
        ValenceElementData(Element("O"), -2),
    ]

    ValenceElement.extend_data(V)

    print(ValenceElement(0))  # 输出: Fe(+2)
    print(ValenceElement("Fe(+2)"))  # 同上
    print(ValenceElement((Element("Fe"), 3)))  # 输出: Fe(+3)
    print(ValenceElement("O(-2)"))  # 输出: O(-2)

    try:
        ValenceElement.new_valence_element(ValenceElementData(Element("Fe"), 2))
    except ValueError as e:
        print(e)  # 价态冲突: Fe_2 已用于索引 0 (Iron(II))

    ValenceElement.clear_data()
    print(len(ValenceElement.registry))  # 输出: 0
