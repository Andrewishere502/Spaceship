import datetime

from projectiles import IonProjectile
from .abstract_weapon import AbstractWeapon


class IonFlak(AbstractWeapon[IonProjectile]):
    def __init__(self):
        weapon_name = 'ion flak'
        image_name = 'ion-flak.png'
        max_ammo = 800  # 100 shots of 8
        ammo_per_use = 8
        ammo_spread = 30
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
