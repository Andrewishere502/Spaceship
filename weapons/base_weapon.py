import datetime
from pathlib import Path
import random

import pygame
from pygame import Vector2

from components import (
    Movement,
    Artist,
)
from utils import (
    CooldownTimer,
    BoundedFloat,
)


class BaseWeapon[ProjectileType]:
    def __init__(
        self,
        weapon_name: str,
        image_name: str,
        projectile_class: type[ProjectileType],
        projectile_speed: float,
        projectile_spread: float,
        max_ammo: int,
        ammo_per_use: int,
        fire_rate: datetime.timedelta,
    ) -> None:
        """
        Instantiate the new weapon.

        :param weapon_name:
        :type weapon_name: str
        :param image_name: 
        :type image_name: str
        :param projectile_class:
        :type projectile_class: type[ProjectileType]
        :param projectile_speed: Speed of the projectiles relative to
            the weapon when they are fired.
        :type projectile_speed: float
        :param projectile_spread: How much the angle of the created
            projectile may deviate from the base angle, centered on
            `base_angle`. In other words, the initial angle of a
            produced projectile may be `base_angle - projectile_spread / 2`
            to `base_angle + projectile_spread / 2`.
        :type projectile_spread: float
        :param max_ammo:
        :type max_ammo: int
        :param ammo_per_use:
        :type ammo_per_use: int
        :param fire_rate:
        :type fire_rate: datetime.timedelta
        """
        weapon_image_dir = Path('Sprites', 'Weapons')
        image_path = weapon_image_dir / image_name
        self.image = pygame.image.load(image_path)

        item_image_path = weapon_image_dir / 'items' / image_name
        self._item_image_path = item_image_path
        self.item_artist = Artist(item_image_path)

        self.name = weapon_name

        self._projectile_class = projectile_class
        self._projectile_speed = projectile_speed
        self._projectile_spread = projectile_spread

        self._ammo = BoundedFloat(
            max_ammo,
            0,
            max_ammo
        )
        self.ammo_per_use = ammo_per_use

        self._cooldown_timer = CooldownTimer(fire_rate)
        # Start the cooldown timer in the ready state.
        self._cooldown_timer.start(is_ready=True)
        return

    def get_item_image(self, angle: float) -> pygame.surface.Surface:
        return self.item_artist.get_image(angle)

    def fire(
        self,
        initial_pos: Vector2,
        base_vel: Vector2,
        base_angle: float,
    ) -> list[ProjectileType]:
        """
        Return a list of projectiles produced by the weapon.

        :param initial_pos: Initial position of the projectile.
        :type initial_pos: Vector2
        :param base_vel: Base velocity of the weapon, used to calculate
            the initial velocity of the projectile(s) relative to the
            frame of reference the weapon exists in.
        :type base_vel: Vector2
        :param base_angle: Base angle for the projectile.
        :type base_angle: float
        :return: A list of projectiles.
        :rtype: list[ProjectileType]
        """

        # Return no projectiles if the cooldown isn't ready yet.
        is_ready = self._cooldown_timer.get_is_ready()
        if not is_ready:
            return []

        # Limit the number of projectiles fired to the ammo remaining.
        num_projectiles = min(int(self._ammo.value), self.ammo_per_use)
        if num_projectiles == 0:
            return []

        # Calculate the minimum and maximum projectile angle.
        min_angle = base_angle - self._projectile_spread / 2
        max_angle = base_angle + self._projectile_spread / 2


        # Create one projectile for the number of projectiles that
        # should be fired.
        projectiles = []
        for _ in range(num_projectiles):
            initial_angle = self._get_random_float(min_angle, max_angle)

            added_vel = Movement.make_vector2(
                self._projectile_speed,
                initial_angle,
            )
            # Reflect across y-axis since negative is up.
            added_vel = Movement.reflect_y_axis(added_vel)
            # Calculate the initial velocity, taking into account
            initial_vel = base_vel + added_vel

            projectile = self._projectile_class(
                initial_pos,  # type: ignore
                initial_vel,
                initial_angle,
            )
            projectiles.append(projectile)

        # Reduce the ammo level by how much was used.
        self.adjust_ammo(-num_projectiles)

        # Start the weapon's cooldown again.
        self._cooldown_timer.start()
        return projectiles

    def adjust_ammo(self, delta_ammo: int) -> None:
        """
        Adjust the current ammo level by the given amount (positive or
        negative). Cannot decrease ammo

        :param delta_ammo: The amount of ammo to increase/decrease the
            current ammo level by. Positive to increase ammo, negative
            to decrease ammo.
        :type delta_ammo: int
        """
        self._ammo += delta_ammo
        return

    def refill(self) -> None:
        """
        Completely refill the weapon's ammo.
        """
        # Fill the ammo to max. It will be clipped to avoid exceeding
        # the maximum allowed ammo.
        self.adjust_ammo(int(self._ammo.max_value))
        return

    def get_ammo_ratio(self) -> float:
        """
        Return the ratio of current ammo to maximum ammo.
        """
        return self._ammo.get_normalized()

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

    @property
    def is_ready(self) -> bool:
        """
        Return `True` if the weapon can fire, otherwise return `False`.
        """
        return self._cooldown_timer.get_is_ready()
