import datetime

from projectiles import PlasmaProjectile
from .abstract_weapon import AbstractWeapon


class PlasmaLauncher(AbstractWeapon[PlasmaProjectile]):
    def __init__(self):
        weapon_name = 'plasma launcher'
        image_name = 'plasma-launcher.png'
        max_ammo = 50
        ammo_per_use = 1
        ammo_spread = 0
        fire_rate = datetime.timedelta(milliseconds=100)
        super().__init__(
            weapon_name,
            image_name,
            PlasmaProjectile,
            max_ammo,
            ammo_per_use,
            ammo_spread,
            fire_rate,
        )
        return
