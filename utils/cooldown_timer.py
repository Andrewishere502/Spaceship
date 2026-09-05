import datetime


class CooldownTimer:
    """
    Timer for managing a cooldown.
    """
    def __init__(
        self,
        threshold: datetime.timedelta,
    ) -> None:
        """
        Initialize the new `CooldownTimer` instance.

        :param threshold: How long the timer must run since starting
            before it indicates ready again.
        :type threshold: datetime.timedelta
        """
        self.__threshold = threshold
        self.start()
        return

    def get_is_ready(
        self,
        reference_datetime: datetime.datetime | None = None
    ) -> bool:
        """
        Return `True` if the difference between the given reference
        timestamp and when the timer was started meets or exceeds the
        required threshold in milliseconds. Otherwise return `False`.

        :param reference_datetime: Some timestamp. Set to the current
            datetime if `None`.
        :type reference_datetime: datetime.datetime | None, default
            `None`
        :return: Whether the timer is ready or not.
        :rtype: bool
        """
        if reference_datetime is None:
            reference_datetime = datetime.datetime.now()
        return self.get_timedelta(reference_datetime) >= self.__threshold

    def get_timedelta(
        self,
        reference_datetime: datetime.datetime | None = None
    ) -> datetime.timedelta:
        """
        Return the time since the timer was started relative to the
        given timestamp.

        :param reference_datetime: Some datetime. Set to the current
            datetime if `None`.
        :type reference_datetime: datetime.datetime | None, default
            `None`
        :return: Time since the timer was started relative to
            `reference_datetime`. Relative to right now if
            `reference_datetime` is `None`.
        :rtype: datetime.timedelta
        """
        if reference_datetime is None:
            reference_datetime = datetime.datetime.now()
        return reference_datetime - self.__started_at

    def start(self) -> datetime.datetime:
        """
        Record the current timestamp as the new starting point for the
        timer.

        :return: Timestamp set as the timer's new start.
        :rtype: datetime.datetime
        """
        self.__started_at = datetime.datetime.now()
        return self.__started_at
