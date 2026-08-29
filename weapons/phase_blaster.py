from pygame import Vector2

from projectiles import PhaserProjectile
from .abstract_weapon import AbstractWeapon


class PhaseBlaster(AbstractWeapon[PhaserProjectile]):
    def __init__(self):
        weapon_name = 'phase blaster'
        image_name = 'phase-blaster.png'
        max_ammo = 200
        ammo_per_use = 1
        super().__init__(
            weapon_name,
            image_name,
            PhaserProjectile,
            max_ammo,
            ammo_per_use,
        )
        return

    def fire(
        self,
        initial_pos: Vector2,
        base_angle: float,
    ) -> list[PhaserProjectile]:
        """
        Return a list with a single `PhaserProjectile` pointed in the
        direction of `base_angle`.

        :param initial_pos: Initial position of the projectile.
        :type initial_pos: Vector2
        :param base_angle: Base angle to fire the projectile at.
        :type base_angle: float
        :return: List with a single projectile instance.
        :rtype: list[PhaserProjectile]
        """
        return self._make_projectiles(initial_pos, base_angle)
