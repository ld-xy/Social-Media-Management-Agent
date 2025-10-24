from typing import Any


class Base_Tool:
    """
    这是一个基础的工具类
    """

    def __init__(self) -> None:
        pass

    def forward(self, input_data):
        pass

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass
