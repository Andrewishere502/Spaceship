from pygame import Vector2

from projectiles import IonProjectile
from .abstract_weapon import AbstractWeapon


class IonRing(AbstractWeapon[IonProjectile]):
    def __init__(self):
        weapon_name = 'ion ring'
        image_name = 'ion-ring.png'
        max_ammo = 720  # 10 shots of 72
        ammo_per_use = 72
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
        Return a list of 72 `IonProjectile` instances, spread randomly
        in a 360 degree circle.

        :param initial_pos: Initial position of the projectile.
        :type initial_pos: Vector2
        :param base_angle: Base angle to fire the projectile at.
            Doesn't affect the projectiles since they are spread out
            in a full 360 degree circle.
        :type base_angle: float
        :return: List with a single projectile instance.
        :rtype: list[IonProjectile]
        """
        ANGLE_SPREAD = 360
        projectiles = self._make_projectiles(
            initial_pos,
            base_angle,
            ANGLE_SPREAD
        )
        return projectiles
