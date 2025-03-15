from __future__ import annotations
import threading
from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class ElementData:
    """化学元素的基础数据类"""

    symbol: str | None = None
    name: str | None = None
    atomic_weight: float | None = None


class Element:
    """表示化学元素的类，提供原子数据存储和原子访问。

    属性：
        registry: 类变量，注册所有元素实例
        symbol_dictionary: 类变量，符号到索引的映射
    """

    registry: ClassVar[list[Element]] = []
    symbol_dictionary: ClassVar[dict[str, int]] = {}
    _lock: ClassVar[threading.Lock] = threading.Lock()
    
    index: int
    data: ElementData
    symbol: str

    def __new__(
        cls, identifier: int | str | None = None, data: ElementData | None = None
    ) -> Element:
        """通过标识符获取或创建新元素实例。

        Args:
            identifier: 元素标识符（索引或符号），创建新元素时应为None
            data: 元素数据对象，仅用于创建新实例时

        Returns:
            元素实例

        Raises:
            ValueError: 输入参数无效或符号冲突时
            IndexError: 索引越界时
            KeyError: 符号不存在时
        """
        if data is None:
            if identifier is None:
                raise ValueError("必须提供标识符（整数索引或字符串符号）")

            if isinstance(identifier, int):
                if not 0 <= identifier < len(cls.registry):
                    raise IndexError(
                        f"元素索引越界: {identifier} (有效范围 0-{len(cls.registry)-1})"
                    )
                return cls.registry[identifier]

            if isinstance(identifier, str):
                if identifier not in cls.symbol_dictionary:
                    raise KeyError(f"元素符号不存在: '{identifier}'")
                return cls.registry[cls.symbol_dictionary[identifier]]

            raise TypeError("无效标识符类型，应为int或str")

        with cls._lock:
            new_index = len(cls.registry)
            instance = super().__new__(cls)
            instance._init(new_index, data)

            if instance.symbol in cls.symbol_dictionary:
                existing_index = cls.symbol_dictionary[instance.symbol]
                raise ValueError(
                    f"符号冲突: {instance.symbol}，已用于索引 {existing_index} "
                )

            cls.registry.append(instance)
            cls.symbol_dictionary[instance.symbol] = instance.index
            return instance

    def generate_symbol(self) -> None:
        return self.data.symbol if self.data.symbol else f"<Element {self.index}>"

    def _init(self, index: int, data: ElementData) -> None:
        """内部初始化方法，避免__init__被多次调用"""
        self.index = index
        self.data = data

        self.symbol = self.generate_symbol()

    def __repr__(self) -> str:
        return self.symbol

    @classmethod
    def new_element(cls, data: ElementData) -> Element:
        """创建新元素实例的工厂方法。

        Args:
            data: 包含元素数据的ElementData对象

        Returns:
            新创建的元素实例
        """
        return cls(None, data)  # type: ignore

    @classmethod
    def extend_data(cls, data_list: list[ElementData]) -> list[Element]:
        """批量创建多个元素实例。

        Args:
            data_list: ElementData对象列表

        Returns:
            新创建的元素实例列表
        """
        return [cls.new_element(data) for data in data_list]

    @classmethod
    def clear_data(cls) -> None:
        """清空所有注册数据"""
        with cls._lock:
            cls.registry.clear()
            cls.symbol_dictionary.clear()


if __name__ == "__main__":
    # 测试正常用例
    oxygen_data = ElementData(None, "Oxygen", 15.999)
    hydrogen_data = ElementData("H", "Hydrogen", 1.008)

    oxygen = Element.new_element(oxygen_data)
    hydrogen = Element.new_element(hydrogen_data)

    print(Element(0))  # 输出: O
    print(Element(0) is oxygen)
    print(Element("H").data.name)  # 输出: Hydrogen

    try:
        Element(2)
    except IndexError as e:
        print(e)  # 元素索引越界: 2 (有效范围 0-1)

    try:
        Element("He")
    except KeyError as e:
        print(e)  # 元素符号不存在: 'He'

    try:
        Element.new_element(ElementData("O", "Other Oxygen", 16.0))
    except ValueError as e:
        print(e)  # 符号冲突: 'O' 已用于索引 0 (Oxygen)
