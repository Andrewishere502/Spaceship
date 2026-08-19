from pathlib import Path

import pygame
from pygame import Vector2

from entity import Entity


class Projectile(Entity):
    def __init__(
        self,
        image_name: str,
        initial_pos: Vector2,
        initial_vel: Vector2,
        initial_angle: float,
        max_vel_component: float,
        damage: float,
        tick_life: int,
    ):
        IMAGE_PATH = Path('Sprites', 'Projectiles', image_name)

        super().__init__(
            IMAGE_PATH,
            initial_pos=initial_pos,
            initial_vel=initial_vel,
            initial_angle=initial_angle,
            initial_avel=0,
            max_vel_component=max_vel_component,
            max_avel=0,
        )

        self.damage = damage  # sizes to decrease asteroid by
        self.tick_life = tick_life
        return

    def step(self, dt: float) -> None:
        """
        Update the projectile's movement component.
        """
        super().step(dt)

        self.tick_life -= 1
        return

    @property
    def dead(self):
        return self.tick_life <= 0