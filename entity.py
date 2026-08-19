from pathlib import Path

import pygame
from pygame import Vector2

from components import Movement


class Entity(pygame.sprite.Sprite):
    def __init__(
        self,
        image_path: Path,
        initial_pos: Vector2,
        initial_vel: Vector2,
        initial_angle: float,
        initial_avel: float,
        max_vel_component: float,
        max_avel: float,
    ):
        super().__init__()

        self.movement = Movement(
            initial_pos=initial_pos,
            initial_vel=initial_vel,
            initial_angle=initial_angle,
            initial_avel=initial_avel,
            max_vel_component=max_vel_component,
            max_avel=max_avel,
        )

        self.base_image = pygame.image.load(image_path).convert_alpha()
        return

    def get_image(self):
        image = pygame.transform.rotate(
            self.base_image,
            self.movement.get_angle(),
        )
        return image

    def get_hitbox(self):
        pos = self.movement.get_pos()
        hb_width = self.base_image.get_width()
        hb_height = self.base_image.get_height()
        rect = pygame.Rect(pos.x, pos.y, hb_width, hb_height)
        rect.center = (pos.x, pos.y)
        return rect

    def step(self, dt: float) -> None:
        """
        Update the entity's movement component.
        """
        self.movement.step(dt)
        return
