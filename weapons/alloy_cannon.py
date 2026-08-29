from pygame import Vector2

from projectiles import AlloyProjectile
from .abstract_weapon import AbstractWeapon


class AlloyCannon(AbstractWeapon[AlloyProjectile]):
    def __init__(self):
        weapon_name = 'alloy cannon'
        image_name = 'alloy-cannon.png'
        max_ammo = 100
        ammo_per_use = 1
        super().__init__(
            weapon_name,
            image_name,
            AlloyProjectile,
            max_ammo,
            ammo_per_use,
        )
        return

    def fire(
        self,
        initial_pos: Vector2,
        base_angle: float,
    ) -> list[AlloyProjectile]:
        """
        Return a list with a single `PhaserProjectile` pointed in the
        direction of `base_angle`.

        :param initial_pos: Initial position of the projectile.
        :type initial_pos: Vector2
        :param base_angle: Base angle to fire the projectile at.
        :type base_angle: float
        :return: List with a single projectile instance.
        :rtype: list[AlloyProjectile]
        """
        return self._make_projectiles(initial_pos, base_angle)
