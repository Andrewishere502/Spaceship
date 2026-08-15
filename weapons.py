import random
import pygame

from settings_reader import get_path
from projectiles import PhaserProjectile, PlasmaProjectile, IonProjectile, AlloyProjectile


class Gun:
    def __init__(self, weapon_name, image_name, max_ammo):
        sprite_path = get_path() / 'Weapons' / image_name
        self.name = weapon_name
        self.image = pygame.image.load(sprite_path)
        self.max_ammo = max_ammo
        self.ammo = max_ammo
        return

    def refill(self, ammo):
        self.ammo += ammo
        if self.ammo > self.max_ammo:
            self.ammo = self.max_ammo
        return


class PhaseBlaster(Gun):
    def __init__(self):
        weapon_name = 'phase blaster'
        image_name = 'phase-blaster.png'
        max_ammo = 200
        super().__init__(weapon_name, image_name, max_ammo)
        return

    def fire(self, ship):
        if self.ammo > 0:
            ship_center = ship.center_pos
            projectile_angle = ship.angular_pos

            projectile = PhaserProjectile(ship_center, projectile_angle)
            # shift the projectile's center to the ship's center
            projectile.set_center(ship_center)

            self.ammo -= 1
            return projectile


class PlasmaLauncher(Gun):
    def __init__(self):
        weapon_name = 'plasma launcher'
        image_name = 'plasma-launcher.png'
        max_ammo = 50
        super().__init__(weapon_name, image_name, max_ammo)
        return

    def fire(self, ship):
        if self.ammo > 0:
            ship_center = ship.center_pos
            projectile_angle = ship.angular_pos

            projectile = PlasmaProjectile(ship_center, projectile_angle)
            # shift the projectile's center to the ship's center
            projectile.set_center(ship_center)

            self.ammo -= 1
            return projectile


class IonFlak(Gun):
    def __init__(self):
        weapon_name = 'ion flak'
        image_name = 'ion-flak.png'
        max_ammo = 100
        super().__init__(weapon_name, image_name, max_ammo)
        return

    def fire(self, ship):
        if self.ammo > 0:
            projectiles = []
            ship_center = ship.center_pos
            angle_variability = random.randint(-20, 20)
            projectile_angle = ship.angular_pos + angle_variability

            # projectiles.append(IonProjectile(ship_center, projectile_angle - random.randint(15, 20)))
            projectiles.append(IonProjectile(ship_center, projectile_angle - random.randint(5, 10)))
            projectiles.append(IonProjectile(ship_center, projectile_angle))
            projectiles.append(IonProjectile(ship_center, projectile_angle + random.randint(5, 10)))
            # projectiles.append(IonProjectile(ship_center, projectile_angle + random.randint(15, 20)))

            for projectile in projectiles:
                projectile.set_center(ship_center)
            
            self.ammo -= 1
            return projectiles


class AlloyCannon(Gun):
    def __init__(self):
        weapon_name = 'alloy cannon'
        image_name = 'alloy-cannon.png'
        max_ammo = 100
        super().__init__(weapon_name, image_name, max_ammo)
        return

    def fire(self, ship):
        if self.ammo > 0:
            ship_center = ship.center_pos
            angle_variability = random.randint(-6, 6)
            projectile_angle = ship.angular_pos + angle_variability

            projectile = AlloyProjectile(ship_center, projectile_angle)
            # shift the projectile's center to the ship's center
            projectile.set_center(ship_center)

            self.ammo -= 1
            return projectile


class IonRing(Gun):
    def __init__(self):
        weapon_name = 'ion ring'
        image_name = 'ion-ring.png'
        max_ammo = 10
        super().__init__(weapon_name, image_name, max_ammo)   
        return

    def fire(self, ship):
        if self.ammo > 0:
            projectiles = []
            ship_center = ship.center_pos

            burst_count = 36
            for i in range(burst_count):
                projectile_angle = ship.angular_pos + 360 / burst_count * i
                projectile = IonProjectile(ship_center, projectile_angle)
                projectiles.append(projectile)
                projectile.set_center(ship_center)
            
            self.ammo -= 1
            return projectiles
