from pathlib import Path

from pygame import Vector2

from weapons import (
    Projectile,
    PhaseBlaster,
    PlasmaLauncher,
    IonFlak,
    AlloyCannon,
    IonRing,
)
from entity import Entity
from components import Health


class Spaceship(Entity):
    def __init__(
        self,
        initial_pos: Vector2,
        health: float,
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

        self.health = Health(health, health)

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

    def damage(self, hp: float) -> None:
        self.health.reduce(hp)
        return

    def heal(self, hp: float) -> None:
        self.health.increase(hp)
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

    def fire_weapon(self) -> list[Projectile]:
        return self.weapon.fire(
            self.movement.get_pos(),
            self.movement.get_angle(),
        )

    @property
    def is_alive(self) -> bool:
        return self.health.is_alive

    @property
    def weapon(self):
        return self.weapons_array[self.weapon_index]


