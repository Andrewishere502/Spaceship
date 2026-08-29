from components import (
    Health,
)


class TestHealth:
    """
    Test suite for `Health` class found in
    `components/health.py`.
    """
    def test_increase_hitpoints_partial(self):
        """
        Test behavior when increasing hitpoints only partially, not all
        the way to full health.
        """
        HITPOINTS = 50
        MAX_HITPOINTS = 100

        health = Health(
            HITPOINTS,
            MAX_HITPOINTS,
        )

        # Adjust health from 50 to 60.
        health.adjust_hitpoints(10)

        assert health.hitpoints == HITPOINTS + 10, \
            'Did not heal exactly 10 hp'

        assert health.get_hp_ratio() == 0.6, \
            'Did not heal to exactly 60% (from 50%)'

        assert health.is_alive, 'Should be alive'
        return

    def test_increase_hitpoints_full(self):
        """
        Test behavior when increasing hitpoints to the maximum.
        """
        HITPOINTS = 50
        MAX_HITPOINTS = 100

        health = Health(
            HITPOINTS,
            MAX_HITPOINTS,
        )

        # Adjust health from 50 to 100.
        health.adjust_hitpoints(MAX_HITPOINTS)

        assert health.hitpoints == MAX_HITPOINTS, \
            'Did not heal to exactly maximum hitpoints'

        assert health.get_hp_ratio() == 1.0, \
            'Did not heal to exactly 100% (from 50%)'

        assert health.is_alive, 'Should be alive'
        return

    def test_decrease_hitpoints_partial(self):
        """
        Test behavior when decreasing hitpoints only partially, not all
        the way to zero.
        """
        HITPOINTS = 50
        MAX_HITPOINTS = 100

        health = Health(
            HITPOINTS,
            MAX_HITPOINTS,
        )

        # Damage 10 hp, from 50 to 40.
        health.adjust_hitpoints(-10)

        assert health.hitpoints == HITPOINTS - 10, \
            'Did not take exactly 10 hp damage'

        assert health.get_hp_ratio() == 0.4, \
            'Did not damage to exactly 40% (from 50%)'

        assert health.is_alive, 'Should be alive'
        return

    def test_decrease_hitpoints_full(self):
        """
        Test behavior when decreasing hitpoints only partially, not all
        the way to zero.
        """
        HITPOINTS = 50
        MAX_HITPOINTS = 100

        health = Health(
            HITPOINTS,
            MAX_HITPOINTS,
        )

        # Damage from 50% to 0%.
        health.adjust_hitpoints(-MAX_HITPOINTS)

        assert health.hitpoints == 0, \
            'Did not take damage to exactly 0'

        assert health.get_hp_ratio() == 0.0, \
            'Did not damage to exactly 0% (from 40%)'

        assert not health.is_alive, 'Should not be alive'
        return
