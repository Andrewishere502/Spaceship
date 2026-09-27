import datetime
from dataclasses import (
    dataclass,
    field,
)
from collections.abc import (
    Callable,
    Sequence,
    Mapping,
)
from typing import Any


@dataclass(order=True)
class Event:
    """
    Class which defines some event that should take place in the game.

    :param timestamp: The relative time this event should be triggered.
    :type timestamp: datetime.timedelta
    :param func: Some callable, called when the `Event` instance is
        called.
    :type func: Callable[..., Any]
    :param func_args: Positional arguments passed to the `func`
        callable when the `Event` instance is called.
    :type func_args: Sequence[Any] | None, default `None`
    :param func_kwargs: Keyword arguments passed to the `func`
        callable when the `Event` instance is called.
    :type func_kwargs: Mapping[str, Any] | None, default `None`
    :param num_calls: The number of times to call the `func` when the
        `Event` instance is called.
    :type num_calls: int, default 1
    """
    timestamp: datetime.timedelta = field(compare=True)
    func: Callable[..., Any] = field(compare=False)
    func_args: Sequence[Any] = field(default_factory=list, compare=False)
    func_kwargs: Mapping[str, Any] = field(default_factory=dict, compare=False)
    num_calls: int = field(default=1)

    def __call__(self, *args: Any, **kwargs: Any) -> None:
        """
        Call the underlying callable (`func`) n times (`num_calls`)
        times.
        Unpacking the following to pass as parameters, in order:
            1. The `func_args` given during initialization.
            2. The `args` passed to this method.
            3. The `func_kwargs` given during initialization.
            4. The `kwargs` passed to this method.

        :param args: Positional arguments passed to the underlying
            callable.
        :type args: Any
        :param kwargs: Keyword arguments passed to the underlying
            callable.
        :type kwargs: Any
        """
        for _ in range(self.num_calls):
            self.func(
                *self.func_args,
                *args,
                *self.func_kwargs,
                **kwargs,
            )
        return
