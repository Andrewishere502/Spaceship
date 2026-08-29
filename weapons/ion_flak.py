import datetime

from projectiles import IonProjectile
from .base_weapon import BaseWeapon


class IonFlak(BaseWeapon[IonProjectile]):
    def __init__(self):
        weapon_name = 'ion flak'
        image_name = 'ion-flak.png'
        projectile_speed = 0.4
        projectile_spread = 30
        max_ammo = 800  # 100 shots of 8
        ammo_per_use = 8
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
