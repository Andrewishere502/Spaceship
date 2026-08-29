from abc import (
    ABC,
    abstractmethod,
)
from pathlib import Path
import random

import pygame
from pygame import Vector2


class AbstractWeapon[ProjectileType](ABC):
    def __init__(
        self,
        weapon_name: str,
        image_name: str,
        projectile_class: type[ProjectileType],
        max_ammo: int,
        ammo_per_use: int,
    ) -> None:
        image_path =  Path('Sprites', 'Weapons', image_name)
        self.image = pygame.image.load(image_path)

        self._projectile_class = projectile_class

        self.name = weapon_name

        self.max_ammo = max_ammo
        self.ammo = max_ammo
        self.ammo_per_use = ammo_per_use
        return

    def get_ammo_ratio(self) -> float:
        """
        Return the ratio of current ammo to maximum ammo.
        """
        return self.ammo / self.max_ammo

    def adjust_ammo(self, delta_ammo: int) -> None:
        """
        Adjust the current ammo level by the given amount (positive or
        negative). Cannot decrease ammo

        :param delta_ammo: The amount of ammo to increase/decrease the
            current ammo level by. Positive to increase ammo, negative
            to decrease ammo.
        :type delta_ammo: int
        """
        self.ammo += delta_ammo
        # Cap ammo to minimum 0.
        self.ammo = max(self.ammo, 0)
        # Cap ammo to maximum `self.max_ammo`.
        self.ammo = min(self.ammo, self.max_ammo)
        return

    @abstractmethod
    def fire(
        self,
        initial_pos: Vector2,
        base_angle: float,
    ) -> list[ProjectileType]:
        """
        Return a list of projectiles fired from the weapon.
        """

    def _make_projectiles(
        self,
        initial_pos: Vector2,
        base_angle: float,
        angle_spread: float = 0,
    ) -> list[ProjectileType]:
        """
        Return a list of `n` projectiles, where `n` is the ammo per use
        or the ammo remaining, whichever is less.

        :param initial_pos: Initial position of the projectile.
        :type initial_pos: Vector2
        :param base_angle: Base angle for the projectile.
        :type base_angle: float
        :param angle_spread: How much the angle of the created
            projectile may deviate from the base angle, centered on
            `base_angle`. In other words, the initial angle of a
            produced projectile may be `base_angle - angle_spread / 2`
            to `base_angle + angle_spread / 2`.
        :type angle_spread: float
        :return: A list of projectiles.
        :rtype: list[ProjectileType]
        """

        # Limit the number of projectiles fired to the ammo remaining.
        num_projectiles = min(self.ammo, self.ammo_per_use)
        if num_projectiles == 0:
            return []

        # Calculate the minimum and maximum projectile angle.
        min_angle = base_angle - angle_spread / 2
        max_angle = base_angle + angle_spread / 2

        # Create one projectile for the number of projectiles that
        # should be fired.
        projectiles = []
        for _ in range(num_projectiles):
            initial_angle = self._get_random_float(min_angle, max_angle)
            projectile = self._projectile_class(
                initial_pos,  # type: ignore
                initial_angle,
            )
            projectiles.append(projectile)

        # Reduce the ammo level by how much was used.
        self.adjust_ammo(-num_projectiles)
        return projectiles

    @staticmethod
    def _get_random_float(
        min_value: float,
        max_value: float,
    ) -> float:
        """
        Return a value between the given minimum and maximum.

        :param min_value: Minimum value to return.
        :type min_value: float
        :param max_value: Maximum value to return. Not inclusive.
        :type max_value: float
        """
        if min_value > max_value:
            raise ValueError(
                '`min_value` cannot be greater than `max_value`'
            )
        return min_value + random.random() * (max_value - min_value)
