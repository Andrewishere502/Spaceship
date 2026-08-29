import datetime

from projectiles import IonProjectile
from .abstract_weapon import AbstractWeapon


class IonRing(AbstractWeapon[IonProjectile]):
    def __init__(self):
        weapon_name = 'ion ring'
        image_name = 'ion-ring.png'
        max_ammo = 720  # 10 shots of 72
        ammo_per_use = 72
        ammo_spread = 360
        fire_rate = datetime.timedelta(milliseconds=100)
        super().__init__(
            weapon_name,
            image_name,
            IonProjectile,
            max_ammo,
            ammo_per_use,
            ammo_spread,
            fire_rate,
        )
        return
