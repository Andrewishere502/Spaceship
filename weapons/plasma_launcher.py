import datetime

from projectiles import PlasmaProjectile
from .base_weapon import BaseWeapon


class PlasmaLauncher(BaseWeapon[PlasmaProjectile]):
    def __init__(self):
        weapon_name = 'plasma launcher'
        image_name = 'plasma-launcher.png'
        projectile_speed = 0.2
        projectile_spread = 0
        max_ammo = 50
        ammo_per_use = 1
        fire_rate = datetime.timedelta(milliseconds=100)
        super().__init__(
            weapon_name,
            image_name,
            PlasmaProjectile,
            projectile_speed,
            projectile_spread,
            max_ammo,
            ammo_per_use,
            fire_rate,
        )
        return
