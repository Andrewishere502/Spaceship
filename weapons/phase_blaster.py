import datetime

from projectiles import PhaserProjectile
from .base_weapon import BaseWeapon


class PhaseBlaster(BaseWeapon[PhaserProjectile]):
    def __init__(self):
        weapon_name = 'phase blaster'
        image_name = 'phase-blaster.png'
        projectile_speed = 0.3
        projectile_spread = 0
        max_ammo = 200
        ammo_per_use = 1
        fire_rate = datetime.timedelta(milliseconds=70)
        super().__init__(
            weapon_name,
            image_name,
            PhaserProjectile,
            projectile_speed,
            projectile_spread,
            max_ammo,
            ammo_per_use,
            fire_rate,
        )
        return
