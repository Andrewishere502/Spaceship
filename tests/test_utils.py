import datetime

from utils import (
    BoundedFloat,
    CooldownTimer,
)


class TestBoundedFloat:
    """
    Test suite for `BoundedFloat` class found in
    `utils/bounded_float.py`.
    """
    def test_eq(self):
        """
        Test behavior when comparing the value using the `==` operator.
        """
        INITIAL_VALUE = 50
        MIN_VALUE = 0
        MAX_VALUE = 100

        value = BoundedFloat(
            INITIAL_VALUE,
            MIN_VALUE,
            MAX_VALUE,
        )

        assert value == INITIAL_VALUE, \
            'Value does not equal float of same value'
        assert INITIAL_VALUE == value, \
            'Value does not equal float of same value'
        return

    def test_gt(self):
        """
        Test behavior when comparing the value using the `>` operator.
        """
        INITIAL_VALUE = 50
        MIN_VALUE = 0
        MAX_VALUE = 100

        value = BoundedFloat(
            INITIAL_VALUE,
            MIN_VALUE,
            MAX_VALUE,
        )

        assert not (value > INITIAL_VALUE + 1), \
            'Value greater than a larger float'
        assert value > INITIAL_VALUE - 1, \
            'Value not greater than a smaller float'
        return

    def test_addition(self):
        """
        Test behavior when adding to the value.
        """
        INITIAL_VALUE = 0
        MIN_VALUE = 0
        MAX_VALUE = 100

        value = BoundedFloat(
            INITIAL_VALUE,
            MIN_VALUE,
            MAX_VALUE,
        )

        # Test normal addition that shouldn't trigger clipping.
        assert value + 1 == INITIAL_VALUE + 1, \
            'Value clipped to maximum when shouldn\'t have'

        # Test addition that shoulld trigger clipping.
        assert value + MAX_VALUE * 2 == MAX_VALUE, \
            'Value not properly clipped to maximum'
        return

    def test_subtraction(self):
        """
        Test behavior when subtracting from the value.
        """
        INITIAL_VALUE = 100
        MIN_VALUE = 0
        MAX_VALUE = 100

        value = BoundedFloat(
            INITIAL_VALUE,
            MIN_VALUE,
            MAX_VALUE,
        )

        # Test normal addition that shouldn't trigger clipping.
        assert value - 1 == INITIAL_VALUE - 1, \
            'Value clipped to minimum when shouldn\'t have'

        # Test addition that shoulld trigger clipping.
        assert value - MAX_VALUE * 2 == MIN_VALUE, \
            'Value not properly clipped to minimum'
        return


class TestCooldownTimer:
    """
    Test suite for `CooldownTimer` class found in
    `utils/cooldown_timer.py`.
    """
    def test_ready_state(self):
        """
        Test behavior when the timer runs long enough to meet the
        threshold, overshoot the threshold, and be undershoot the
        threshold.
        """
        DURATION_999_MILLISECONDS = datetime.timedelta(milliseconds=999)
        DURATION_1000_MILLISECONDS = datetime.timedelta(milliseconds=1000)
        DURATION_1001_MILLISECONDS = datetime.timedelta(milliseconds=1001)

        # Set threshold to 1000 milliseconds.
        timer = CooldownTimer(DURATION_1000_MILLISECONDS)

        started_at = timer.start()

        # Get ready state after waiting exactly the threshold time.
        is_ready = timer.get_is_ready(started_at + DURATION_1000_MILLISECONDS)
        assert is_ready, \
            f'Timer ready is {is_ready} despite under threshold'

        # Get ready state after waiting 1 millisecond less than the
        # threshold time.
        is_ready = timer.get_is_ready(started_at + DURATION_999_MILLISECONDS)
        assert not is_ready, \
            f'Timer ready is {is_ready} despite under threshold'

        # Get ready state after waiting 1 millisecond more than the
        # threshold time.
        is_ready = timer.get_is_ready(started_at + DURATION_1001_MILLISECONDS)
        assert is_ready, \
            f'Timer ready is {is_ready} despite under threshold'
        return
