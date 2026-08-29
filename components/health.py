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
        self._hitpoints: float = hitpoints
        self._max_hitpoints: float = max_hitpoints
        return

    def reduce(self, hp: float) -> None:
        """
        Reduce the hitpoints to a minimum of zero.

        :param hp: How much to reduce the current hitpoints by.
        :type hp: float
        """
        # Limit the hitpoints to minimum 0.
        self._hitpoints = max(self._hitpoints - hp, 0)
        return

    def increase(self, hp: float) -> None:
        """
        Increase the hitpoints to a maximum of `max_hitpoints`.

        :param hp: How much to increase the current hitpoints by.
        :type hp: float
        """
        # Limit the hitpoints to minimum 0.
        self._hitpoints = max(self._hitpoints - hp, 0)
        return

    def get_hp_ratio(self) -> float:
        """
        Return the ratio of current hitpoints to maximum hitpoints.
        """
        return self._hitpoints / self._max_hitpoints

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
        return self._hitpoints

    @property
    def max_hitpoints(self) -> float:
        """
        Return the maximum hitpoints.
        """
        return self._max_hitpoints
