from pathlib import Path

import pygame
from pygame import Vector2

from components import (
    Movement,
    Artist,
)


class Entity:
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

        self.artist = Artist(
            image_path,
            is_convert_alpha=True,
        )

        self.movement = Movement(
            initial_pos=initial_pos,
            initial_vel=initial_vel,
            initial_angle=initial_angle,
            initial_avel=initial_avel,
            max_vel_component=max_vel_component,
            max_avel=max_avel,
        )

        return

    def get_image(self) -> pygame.surface.Surface:
        return self.artist.get_image(self.movement.get_angle())

    def get_hitbox(self):
        # Get the unrotated image.
        image = self.artist.get_image(0)

        pos = self.movement.get_pos()
        hb_width = image.get_width()
        hb_height = image.get_height()
        rect = pygame.Rect(pos.x, pos.y, hb_width, hb_height)
        rect.center = (pos.x, pos.y)
        return rect

    def step(self, dt: float) -> None:
        """
        Update the entity's movement component.
        """
        self.movement.step(dt)
        return
