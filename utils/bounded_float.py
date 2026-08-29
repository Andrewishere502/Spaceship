from typing import Self


class BoundedFloat:
    """
    An adjustable value limited between some minimum and maximum,
    including both the minimum and maximum.
    """
    def __init__(
        self,
        value: float,
        min_value: float,
        max_value: float,
    ) -> None:
        """
        Initialize the new `BoundedFloat` instance.
        """
        self.set_min_value(min_value)
        self.set_max_value(max_value)
        # Must set the min/max before calling this method or the
        # `_clip_value` call wil fail.
        self.set_value(value)
        return

    def __eq__(self, obj: object) -> bool:
        """
        Return `True` if the two objects are equal, otherwise return
        `False`.
        """
        if isinstance(obj, (float, int)):
            return self.value == obj
        elif isinstance(obj, self.__class__):
            return self.value == obj.value

        # Return not implemented incase the given object defines a
        # valid `__eq__` method comparing the two.
        return NotImplemented

    def __gt__(self, obj: object) -> bool:
        """
        Return `True` if this object is greater than the given object,
        otherwise return `False`.
        """
        if isinstance(obj, (float, int)):
            return self.value > obj
        elif isinstance(obj, self.__class__):
            return self.value > obj.value

        # Return not implemented incase the given object defines a
        # valid `__gt__` method comparing the two.
        return NotImplemented

    def __add__(self, add_amount: float) -> Self:
        """
        Increase the current value by the given amount.
        """
        self.__value += add_amount
        # Enforce both the minimum and maximum bounds in case the user
        # adds a negative number.
        self._clip_value()
        return self

    def __sub__(self, sub_amount: float) -> Self:
        """
        Decrease the current value by the given amount.
        """
        self.__value -= sub_amount
        # Enforce both the minimum and maximum bounds in case the user
        # subtracts a negative number.
        self._clip_value()
        return self

    def get_normalized(self) -> float:
        """
        Return the current value normalized to between 0 and 1.
        """
        return (self.value - self.min_value) / (self.max_value - self.min_value) 

    def set_value(self, value: float) -> None:
        """
        Set the current value. Requires minimum and maximum values to
        be set already.
        """
        self.__value = value
        # Clip the value to enforce min/max. Requires minimum and
        # maximum values to be set already.
        self._clip_value()
        return

    def set_min_value(self, min_value: float) -> None:
        """
        Set the minimum allowed value.
        """
        self.__min_value = min_value
        return

    def set_max_value(self, max_value: float) -> None:
        """
        Set the minimum allowed value.
        """
        self.__max_value = max_value
        return

    @property
    def value(self) -> float:
        """
        Return the current value.
        """
        return self.__value

    @property
    def min_value(self) -> float:
        """
        Return the minimum value.
        """
        return self.__min_value

    @property
    def max_value(self) -> float:
        """
        Return the maximum value.
        """
        return self.__max_value

    def _clip_value(self) -> None:
        """
        If the value is less than the minimum, set it to the minimum.
        If the value is more than the maximum, set it to the maximum.
        """
        # If the value is less than the minimum, set it to minimum.
        self.__value = max(
            self.value,
            self.min_value,
        )
        # If the value is more than the maximum, set it to maximum.
        self.__value = min(
            self.value,
            self.max_value,
        )
        return
