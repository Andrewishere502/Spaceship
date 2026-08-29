import datetime

from projectiles import PhaserProjectile
from .abstract_weapon import AbstractWeapon


class PhaseBlaster(AbstractWeapon[PhaserProjectile]):
    def __init__(self):
        weapon_name = 'phase blaster'
        image_name = 'phase-blaster.png'
        max_ammo = 200
        ammo_per_use = 1
        ammo_spread = 0
        fire_rate = datetime.timedelta(milliseconds=100)
        super().__init__(
            weapon_name,
            image_name,
            PhaserProjectile,
            max_ammo,
            ammo_per_use,
            ammo_spread,
            fire_rate,
        )
        return
