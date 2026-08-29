import datetime

from projectiles import AlloyProjectile
from .abstract_weapon import AbstractWeapon


class AlloyCannon(AbstractWeapon[AlloyProjectile]):
    def __init__(self):
        weapon_name = 'alloy cannon'
        image_name = 'alloy-cannon.png'
        max_ammo = 100
        ammo_per_use = 1
        ammo_spread = 0
        fire_rate = datetime.timedelta(milliseconds=100)
        super().__init__(
            weapon_name,
            image_name,
            AlloyProjectile,
            max_ammo,
            ammo_per_use,
            ammo_spread,
            fire_rate,
        )
        return
