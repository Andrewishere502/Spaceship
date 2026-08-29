from utils import BoundedFloat


class Health:
    def __init__(
        self,
        hitpoints: float,
        max_hitpoints: float,
    ) -> None:
        """
        Initialize the `Health` object.

        :param hitpoints: Current hitpoints.
        :type hitpoints: float
        :param max_hitpoints: The maximum hitpoints allowed.
        :type max_hitpoints: float
        """
        self._hitpoints = BoundedFloat(
            hitpoints,
            0,
            max_hitpoints,
        )
        return

    def adjust_hitpoints(self, hp: float) -> None:
        """
        Adjust the hitpoints to a minimum of zero.

        :param hp: How much to adjust the current hitpoints by.
            Positive for increase, negative for decrease.
        :type hp: float
        """
        self._hitpoints += hp
        return

    def get_hp_ratio(self) -> float:
        """
        Return the ratio of current hitpoints to maximum hitpoints.
        """
        return self._hitpoints.get_normalized()

    @property
    def is_alive(self) -> bool:
        """
        Return `True` if the current hitpoints is above 0, otherwise
        `False`.
        """
        return self._hitpoints > 0

    @property
    def hitpoints(self) -> float:
        """
        Return the current hitpoints.
        """
        return self._hitpoints.value

    @property
    def max_hitpoints(self) -> float:
        """
        Return the maximum allowed hitpoints.
        """
        return self._hitpoints.max_value
