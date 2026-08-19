from pathlib import Path
import random

import pygame
from pygame import Vector2

from projectiles import (
    Projectile,
    PhaserProjectile,
    PlasmaProjectile,
    IonProjectile,
    AlloyProjectile,
)


class Gun:
    def __init__(
        self,
        weapon_name,
        image_name,
        max_ammo,
        ammo_per_use,
        projectile_class: type[PhaserProjectile | PlasmaProjectile | IonProjectile | AlloyProjectile]
    ) -> None:
        image_path =  Path('Sprites', 'Weapons', image_name)
        self.image = pygame.image.load(image_path)

        self.projectile_class = projectile_class

        self.name = weapon_name

        self.max_ammo = max_ammo
        self.ammo = max_ammo
        self.ammo_per_use = ammo_per_use
        return

    def refill(self, ammo):
        self.ammo += ammo
        # Limit the ammo to the maximum allowed.
        if self.ammo > self.max_ammo:
            self.ammo = self.max_ammo
        return

    def fire(
        self,
        initial_pos: Vector2,
        initial_angle: float,
    ) -> list[Projectile]:
        if self.ammo <= 0:
            return []

        projectiles = []
        # Limit the number of projectiles fired to the ammo remaining.
        for _ in range(min(self.ammo, self.ammo_per_use)):
            projectile = self.projectile_class(
                initial_pos,
                initial_angle,
            )
            projectiles.append(projectile)

        self.ammo -= self.ammo_per_use
        return projectiles


class PhaseBlaster(Gun):
    def __init__(self):
        weapon_name = 'phase blaster'
        image_name = 'phase-blaster.png'
        max_ammo = 200
        super().__init__(
            weapon_name,
            image_name,
            max_ammo,
            1,
            PhaserProjectile,
        )
        return


class PlasmaLauncher(Gun):
    def __init__(self):
        weapon_name = 'plasma launcher'
        image_name = 'plasma-launcher.png'
        max_ammo = 50
        super().__init__(
            weapon_name,
            image_name,
            max_ammo,
            1,
            PlasmaProjectile,
        )
        return


class IonFlak(Gun):
    def __init__(self):
        weapon_name = 'ion flak'
        image_name = 'ion-flak.png'
        max_ammo = 100
        super().__init__(
            weapon_name,
            image_name,
            max_ammo,
            8,
            IonProjectile,
        )
        return


class AlloyCannon(Gun):
    def __init__(self):
        weapon_name = 'alloy cannon'
        image_name = 'alloy-cannon.png'
        max_ammo = 100
        super().__init__(
            weapon_name,
            image_name,
            max_ammo,
            1,
            AlloyProjectile,
        )
        return


class IonRing(Gun):
    def __init__(self):
        weapon_name = 'ion ring'
        image_name = 'ion-ring.png'
        max_ammo = 10
        super().__init__(
            weapon_name,
            image_name,
            max_ammo,
            36,
            IonProjectile,
        )
        return

    # def fire(self, ship):
    #     if self.ammo > 0:
    #         projectiles = []
    #         ship_center = ship.movement.get_pos()

    #         burst_count = 36
    #         for i in range(burst_count):
    #             projectile_angle = ship.movement.get_angle() + 360 / burst_count * i
    #             projectile = IonProjectile(ship_center, projectile_angle)
    #             projectiles.append(projectile)
            
    #         self.ammo -= 1
    #         return projectiles
