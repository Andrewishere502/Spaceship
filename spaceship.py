from pathlib import Path

from pygame import Vector2

from weapons import (
    PhaseBlaster,
    PlasmaLauncher,
    IonFlak,
    AlloyCannon,
    IonRing,
)
from entity import Entity
from components import Health


type WeaponType = (
    PhaseBlaster
    | PlasmaLauncher
    | IonFlak
    | AlloyCannon
    | IonRing
)


class Spaceship(Entity):
    def __init__(
        self,
        initial_pos: Vector2,
        initial_health: float,
    ):
        IMAGE_PATH = Path('Sprites/spaceship-2.png')
        MAX_VEL_COMPONENT = 0.1

        super().__init__(
            IMAGE_PATH,
            initial_pos=initial_pos,
            initial_vel=Vector2(0, 0),
            initial_angle=0,
            initial_avel=0,
            max_vel_component=MAX_VEL_COMPONENT,
            max_avel=0,
        )

        self.health = Health(initial_health, initial_health)

        self.weapons_array = [
            PhaseBlaster(),
            PlasmaLauncher(),
            IonFlak(),
            AlloyCannon(),
            IonRing(),
        ]
        self.weapon_index = 0
        self.score = 0
        self.asteriods_shot = 0
        return

    def next_weapon(self):
        self.weapon_index += 1
        if self.weapon_index >= len(self.weapons_array):
            self.weapon_index = 0
        return

    def prev_weapon(self):
        self.weapon_index -= 1
        if self.weapon_index < 0:
            self.weapon_index = len(self.weapons_array) - 1
        return

    def fire_weapon(self):
        """
        Fire the spaceship's currently selected weapon.
        """
        new_projectiles = self.get_weapon().fire(
            self.movement.get_pos(),
            self.movement.get_vel(),
            self.movement.get_angle(),
        )
        return new_projectiles

    def get_weapon(self) -> WeaponType:
        """
        Return the currently selected weapon.

        :return: Currently selected weapon.
        :rtype: WeaponType
        """
        return self.weapons_array[self.weapon_index]

    @property
    def is_alive(self) -> bool:
        return self.health.is_alive

