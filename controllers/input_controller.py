from collections.abc import Callable
from typing import Any


class InputController:
    def __init__(self) -> None:
        # Initialize with an empty input map.
        self.set_map({})
        return

    def send(self, key: Any, *args, **kwargs) -> Any:
        func = self._input_map.get(key)
        # Return `None` if the key didn't map to any action.
        if func is None:
            return None
        return func(*args, **kwargs)

    def set_map(self, input_map: dict[Any, Callable]) -> None:
        self._input_map = input_map
        return
