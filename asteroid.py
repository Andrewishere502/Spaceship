from pathlib import Path
import math

import pygame
from pygame import Vector2

from entity import Entity


class Asteroid(Entity):
    def __init__(
        self,
        initial_pos: Vector2,
        initial_vel: Vector2,
        initial_angle: float,
        initial_avel: float,
        size: int,
    ) -> None:
        IMAGE_PATH = Path('Sprites', 'Asteroids', 'asteroid-{}.png'.format(size))
        MAX_VEL_COMPONENT = 0.15
        MAX_AVEL = 1

        super().__init__(
            IMAGE_PATH,
            initial_pos=initial_pos,
            initial_vel=initial_vel,
            initial_angle=initial_angle,
            initial_avel=initial_avel,
            max_vel_component=MAX_VEL_COMPONENT,
            max_avel=MAX_AVEL,
        )

        self.size = size
        self.set_base_image(size)
        return

    def set_base_image(self, size: int):
        image_path = Path('Sprites', 'Asteroids', 'asteroid-{}.png'.format(size))
        self.base_image = pygame.image.load(image_path).convert_alpha()
        return

    @property
    def damage(self):
        return self.size * 3

    @property
    def point_value(self):
        return self.size * 50

    def split(self, damage: float) -> 'Asteroid':
        vel = self.movement.get_vel()

        # Deflect this astroid in a different direction.
        self.movement.set_vel(vel.rotate(30))

        # Shrink the asteroid by the damage dealt.
        new_size = int(self.size - damage)
        self.size = new_size

        # Reload the image.
        self.set_base_image(self.size)

        # Create a new asteroid deflected away from the original
        # asteroid.
        new_asteroid = Asteroid(
            self.movement.get_pos(),
            vel.rotate(-30),
            self.movement.get_angle(),
            self.movement.get_avel(),
            new_size,
        )
        return new_asteroid
