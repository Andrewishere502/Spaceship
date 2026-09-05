import math
import datetime
from pathlib import Path

from pygame import Vector2

from entity import Entity
from utils import CooldownTimer


class BaseProjectile(Entity):
    def __init__(
        self,
        image_name: str,
        initial_pos: Vector2,
        initial_vel: Vector2,
        initial_angle: float,
        damage: float,
        lifespan: datetime.timedelta,
    ):
        IMAGE_PATH = Path('Sprites', 'Projectiles', image_name)

        super().__init__(
            IMAGE_PATH,
            initial_pos=initial_pos,
            initial_vel=initial_vel,
            initial_angle=initial_angle,
            initial_avel=0,
            max_vel_component=math.sqrt(initial_vel.magnitude()),
            max_avel=0,
        )

        # How much to reduce an asteroid's size by.
        self.damage = damage

        # Use a cooldown timer to track the lifespan of the projectile.
        # Start the lifespan as soon as it is initialized.
        self._lifespan_tracker = CooldownTimer(lifespan)
        self._lifespan_tracker.start()
        return

    def get_is_done(self) -> bool:
        """
        Return `True` if the projectile's lifespan is complete,
        otherwise `False`.
        """
        # If the cooldown timer object "is read" that means the
        # timer has passed the threshold and thus the projectile has
        # reached the end of its lifespan.
        return self._lifespan_tracker.get_is_ready()
