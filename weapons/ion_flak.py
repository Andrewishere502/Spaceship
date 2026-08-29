from pygame import Vector2

from projectiles import IonProjectile
from .abstract_weapon import AbstractWeapon


class IonFlak(AbstractWeapon[IonProjectile]):
    def __init__(self):
        weapon_name = 'ion flak'
        image_name = 'ion-flak.png'
        max_ammo = 800  # 100 shots of 8
        ammo_per_use = 8
        super().__init__(
            weapon_name,
            image_name,
            IonProjectile,
            max_ammo,
            ammo_per_use,
        )
        return

    def fire(
        self,
        initial_pos: Vector2,
        base_angle: float,
    ) -> list[IonProjectile]:
        """
        Return a list of 8 `IonProjectile` instances, spread randomly
        in a 30 degree cone centered on given `base_angle`.

        :param initial_pos: Initial position of the projectile.
        :type initial_pos: Vector2
        :param base_angle: Base angle to fire the projectile at.
        :type base_angle: float
        :return: List with a single projectile instance.
        :rtype: list[IonProjectile]
        """
        ANGLE_SPREAD = 30
        return self._make_projectiles(
            initial_pos,
            base_angle,
            ANGLE_SPREAD
        )