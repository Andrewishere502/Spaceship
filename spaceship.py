import random
from pathlib import Path

import pygame
from pygame import Vector2

from ship import (
    ShipChassis,
    BaseShipModule,
    WeaponSystem,
)
from components import (
    Health,
    Movement,
)
from weapons import BaseWeapon
from projectiles import BaseProjectile


class Spaceship:
    def __init__(
        self,
        initial_pos: Vector2,
        initial_health: float,
        max_health: float,
        weapon_system: WeaponSystem
    ):
        SPACESHIP_SPRITE_DIR = Path('Sprites/spaceships/small/')

        INITIAL_VEL = Vector2(0, 0)
        INITIAL_ANGLE = 0
        INITIAL_AVEL = 0
        MAX_VEL_COMPONENT = 0.13
        MAX_AVEL = 0

        body_module = BaseShipModule(SPACESHIP_SPRITE_DIR / 'body.png')
        left_wing_path = get_random_path(SPACESHIP_SPRITE_DIR / 'wings', '.png')
        left_wing_module = BaseShipModule(left_wing_path)
        right_wing_module = BaseShipModule(
            left_wing_path,
            is_mirror_x=True,
        )
        nose_module = BaseShipModule(
            get_random_path(SPACESHIP_SPRITE_DIR / 'heads', '.png'),
        )
        tail_module = BaseShipModule(
            get_random_path(SPACESHIP_SPRITE_DIR / 'tails', '.png'),
        )

        self.chassis = ShipChassis(
            {
                (5, 8): body_module,
                (0, 0): left_wing_module,
                (0, 24): right_wing_module,
                (24, 8): nose_module,
                (0, 8): tail_module,
            }
        )
        self.chassis.load_base_image()

        self.weapon_system = weapon_system

        self.movement = Movement(
            initial_pos=initial_pos,
            initial_vel=INITIAL_VEL,
            initial_angle=INITIAL_ANGLE,
            initial_avel=INITIAL_AVEL,
            max_vel_component=MAX_VEL_COMPONENT,
            max_avel=MAX_AVEL,
        )

        self.health = Health(
            initial_health,
            max_health,
        )

        self.score = 0
        self.asteriods_shot = 0
        return

    def get_image(self) -> pygame.surface.Surface:
        """
        Return the image of the spaceship.
        """
        angle = self.movement.get_angle()
        image = self.chassis.get_image(angle)

        # Get the weapon item image to draw on the spaceship.
        weapon_item_image = self.weapon_system.get_weapon().get_item_image(angle)

        # Get the position of the weapon item image relative to the
        # chassis image.
        weapon_item_image_pos = image.get_rect().center + self.weapon_system.pos

        # Draw the weapon on top of the spaceship image, aligning their
        # center points.
        image.blit(
            weapon_item_image,
            # Align the weapon to the weapon system's position.
            weapon_item_image.get_rect(center=weapon_item_image_pos)
        )
        return image

    def fire_weapon(self) -> list[BaseProjectile]:
        new_projectiles = self.weapon_system.get_weapon().fire(
            self.movement.get_pos(),
            self.movement.get_vel(),
            self.movement.get_angle(),
        )
        return new_projectiles

    def get_weapon(self) -> BaseWeapon:
        return self.weapon_system.get_weapon()

    def get_hitbox(self):
        # Get the unrotated image.
        image = self.chassis.get_image(0)

        pos = self.movement.get_pos()
        hb_width = image.get_width()
        hb_height = image.get_height()
        rect = pygame.Rect(pos.x, pos.y, hb_width, hb_height)
        rect.center = (pos.x, pos.y)
        return rect

    @property
    def is_alive(self) -> bool:
        return self.health.is_alive


def get_random_path(base_dir: Path, allow_suffix: str) -> Path:
    """
    Return a random file with the provided suffix from the given base
    directory.
    """
    return random.choice(
        list(
            filter(
                lambda file_path: file_path.suffix == allow_suffix,
                base_dir.iterdir(),
            )
        )
    )
