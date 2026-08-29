import math

from pygame import Vector2

from .base_projectile import BaseProjectile


class IonProjectile(BaseProjectile):
    def __init__(
        self,
        initial_pos: Vector2,
        initial_vel: Vector2,
        initial_angle: float,
    ):
        DAMAGE = 1
        TICK_LIFE = 20

        super().__init__(
            'ion-projectile.png',
            initial_pos,
            initial_vel,
            initial_angle,
            DAMAGE,
            TICK_LIFE,
        )
        return

