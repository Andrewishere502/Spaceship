import datetime

from projectiles import IonProjectile
from .base_weapon import BaseWeapon


class IonRing(BaseWeapon[IonProjectile]):
    def __init__(self):
        weapon_name = 'ion ring'
        image_name = 'ion-ring.png'
        projectile_speed = 0.4
        projectile_spread = 360
        max_ammo = 720  # 10 shots of 72
        ammo_per_use = 72
        fire_rate = datetime.timedelta(milliseconds=100)
        super().__init__(
            weapon_name,
            image_name,
            IonProjectile,
            projectile_speed,
            projectile_spread,
            max_ammo,
            ammo_per_use,
            fire_rate,
        )
        return
