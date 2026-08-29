import math

from pygame import Vector2

from .base_projectile import BaseProjectile


class PlasmaProjectile(BaseProjectile):
    def __init__(
        self,
        initial_pos: Vector2,
        initial_vel: Vector2,
        initial_angle: float,
    ):
        DAMAGE = 2
        TICK_LIFE = 80

        super().__init__(
            'plasma-projectile.png',
            initial_pos,
            initial_vel,
            initial_angle,
            DAMAGE,
            TICK_LIFE,
        )
        return