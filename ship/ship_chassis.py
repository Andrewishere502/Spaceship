from collections.abc import Sequence

import pygame
from pygame import Vector2

from projectiles import BaseProjectile
from weapons import (
    BaseWeapon,
    PhaseBlaster,
    PlasmaLauncher,
    IonFlak,
    AlloyCannon,
    IonRing,
)
from components import Movement
from .ship_module import ShipModule
from .weapon_system import WeaponSystem


class ShipChassis:
    def __init__(
        self,
        width: int,
        height: int,
        initial_pos: Vector2,
        initial_vel: Vector2,
        initial_angle: float,
        initial_avel: float,
        max_vel_component: float,
        max_avel: float,
        body_module: ShipModule,
        left_wing_module: ShipModule,
        right_wing_module: ShipModule,
        nose_module: ShipModule,
        tail_module: ShipModule,
        weapon_system: WeaponSystem,
    ):
        self.movement = Movement(
            initial_pos=initial_pos,
            initial_vel=initial_vel,
            initial_angle=initial_angle,
            initial_avel=initial_avel,
            max_vel_component=max_vel_component,
            max_avel=max_avel,
        )

        self._width = width
        self._height = height

        self.weapon_system = weapon_system

        # Define the pieces attached to the chassis to make up the
        # entire spaceship.
        self._ship_modules = [
            body_module,
            left_wing_module,
            right_wing_module,
            nose_module,
            tail_module,
        ]
        self.load_base_image()

        self.score = 0
        self.asteriods_shot = 0
        return

    def step(self, dt: float) -> None:
        """
        Update the entity's movement component.
        """
        self.movement.step(dt)
        return

    def fire_weapon(self) -> Sequence[BaseProjectile]:
        """

        """
        new_projectiles = self.weapon_system.get_weapon().fire(
            self.movement.get_pos(),
            self.movement.get_vel(),
            self.movement.get_angle(),
        )
        return new_projectiles

    def get_image(self) -> pygame.surface.Surface:
        """
        Return the spaceship's image, rotated to the direction the
        spaceship is facing. Includes the currently equiped weapon.
        """
        image = self.get_base_image().copy()

        # Rotate the image in the direction the chassis is facing.
        angle = self.movement.get_angle()
        image = pygame.transform.rotate(image, angle)

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

    def get_weapon(self) -> BaseWeapon:
        return self.weapon_system.get_weapon()

    def get_hitbox(self):
        # Get the unrotated image.
        image = self.get_base_image()

        pos = self.movement.get_pos()
        hb_width = image.get_width()
        hb_height = image.get_height()
        rect = pygame.Rect(pos.x, pos.y, hb_width, hb_height)
        rect.center = (pos.x, pos.y)
        return rect

    def get_base_image(self) -> pygame.surface.Surface:
        """
        Return the base image.
        """
        return self._base_image

    def load_base_image(self) -> None:
        """
        Initialize the base image by combining the images of all ship
        modules onto the same surface.
        """
        # Draw the image of each module onto the base image.
        base_image = pygame.surface.Surface((self._width, self._height))
        base_image = base_image.convert_alpha()
        base_image.fill((0, 0, 0, 0))
        for ship_module in self._ship_modules:
            base_image.blit(
                ship_module.artist.get_image(0),
                ship_module.pos,
            )
        self._base_image = base_image
        return
