import datetime

from projectiles import AlloyProjectile
from .base_weapon import BaseWeapon


class AlloyCannon(BaseWeapon[AlloyProjectile]):
    def __init__(self):
        weapon_name = 'alloy cannon'
        image_name = 'alloy-cannon.png'
        projectile_speed = 0.2
        projectile_spread = 0
        max_ammo = 100
        ammo_per_use = 1
        fire_rate = datetime.timedelta(milliseconds=100)
        super().__init__(
            weapon_name,
            image_name,
            AlloyProjectile,
            projectile_speed,
            projectile_spread,
            max_ammo,
            ammo_per_use,
            fire_rate,
        )
        return
