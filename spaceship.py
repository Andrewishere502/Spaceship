from pathlib import Path
import random

import pygame
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
        SPACESHIP_SPRITE_DIR = Path('Sprites/spaceships/small/')
        MAX_VEL_COMPONENT = 0.13

        body_image_path = SPACESHIP_SPRITE_DIR / 'body.png'
        head_image_path = SPACESHIP_SPRITE_DIR / 'heads'
        left_wing_image_path = SPACESHIP_SPRITE_DIR / 'wings'
        tail_image_path = SPACESHIP_SPRITE_DIR / 'tails'

        super().__init__(
            body_image_path,
            initial_pos=initial_pos,
            initial_vel=Vector2(0, 0),
            initial_angle=0,
            initial_avel=0,
            max_vel_component=MAX_VEL_COMPONENT,
            max_avel=0,
        )

        ####### Configure spaceship image ########
        get_is_png = lambda file_path: file_path.suffix == '.png'
        head_image_path = random.choice(
            list(
                filter(
                    get_is_png,
                    head_image_path.iterdir(),
                )
            )
        )
        left_wing_image_path = random.choice(
            list(
                filter(
                    get_is_png,
                    left_wing_image_path.iterdir(),
                )
            )
        )
        tail_image_path = random.choice(
            list(
                filter(
                    get_is_png,
                    tail_image_path.iterdir(),
                )
            )
        )

        head_pos = (24, 8)
        head_image = pygame.image.load(head_image_path)
        head_rect = head_image.get_rect(topleft=head_pos)

        left_wing_pos = (0, 0)
        left_wing_image = pygame.image.load(left_wing_image_path)
        left_wing_rect = left_wing_image.get_rect(topleft=left_wing_pos)

        right_wing_pos = (0, 24)
        right_wing_image = pygame.transform.flip(
            left_wing_image,
            False,
            True,
        )
        right_wing_rect = right_wing_image.get_rect(topleft=right_wing_pos)

        tail_pos = (0, 8)
        tail_image = pygame.image.load(tail_image_path)
        tail_rect = tail_image.get_rect(topleft=tail_pos)

        self.artist.blit(head_image, head_rect)
        self.artist.blit(left_wing_image, left_wing_rect)
        self.artist.blit(right_wing_image, right_wing_rect)
        self.artist.blit(tail_image, tail_rect)
        #########

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

    def get_image(self) -> pygame.surface.Surface:
        """
        Return the spaceship's image, rotated to the direction the
        spaceship is facing. Includes the currently equiped weapon.
        """
        # Get the angle of rotation for the spaceship.
        angle = self.movement.get_angle()

        # Get the base spaceship image.
        spaceship_image = self.artist.get_image(angle)

        # Get the weapon item image to draw on the spaceship.
        weapon_item_image = self.get_weapon().get_item_image(angle)

        # Draw the weapon on top of the spaceship image, aligning their
        # center points.
        spaceship_image.blit(
            weapon_item_image,
            weapon_item_image.get_rect(center=spaceship_image.get_rect().center)
        )
        return spaceship_image

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

