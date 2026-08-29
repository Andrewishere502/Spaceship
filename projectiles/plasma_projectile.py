import math

from pygame import Vector2

from .base_projectile import BaseProjectile


class PlasmaProjectile(BaseProjectile):
    def __init__(
        self,
        initial_pos: Vector2,
        initial_angle: float,
    ):
        SPEED = 0.2
        DAMAGE = 2
        TICK_LIFE = 80

        # Start pointed directly right, then rotate towards the initial
        # angle.
        initial_vel = Vector2(
            SPEED,
            0
        ).rotate(
            initial_angle
        ).reflect(
            # Reflect accross y-axis since negative Y is up.
            Vector2(
                0,
                1,
            )
        )

        super().__init__(
            'plasma-projectile.png',
            initial_pos,
            initial_vel,
            initial_angle,
            math.sqrt(SPEED),
            DAMAGE,
            TICK_LIFE,
        )
        return