from pathlib import Path

from entity import Entity
from spaceship import Spaceship


class Crate(Entity):
    MAX_VEL_COMPONENT = 0.05
    MAX_AVEL = 0.5

    def __init__(
        self,
        image_path,
        initial_pos,
        initial_vel,
        initial_angle,
        initial_avel,
    ) -> None:
        super().__init__(
            image_path,
            initial_pos,
            initial_vel,
            initial_angle,
            initial_avel,
            self.MAX_VEL_COMPONENT,
            self.MAX_AVEL,
        )
        return


class HealthCrate(Crate):
    def __init__(self, pos, vel, angular_pos, angular_vel):
        image_path = Path('Sprites', 'Crates', 'health-crate.png')
        super().__init__(image_path, pos, vel, angular_pos, angular_vel)
        return

    def do_action(self, spaceship: Spaceship) -> None:
        """
        Heal the spaceship up to full health.

        :param spaceship: The spaceship to heal.
        :type spaceship: Spaceship
        """
        spaceship.health.adjust_hitpoints(spaceship.health.max_hitpoints)
        return


class AmmoCrate(Crate):
    def __init__(self, pos, vel, angular_pos, angular_vel):
        image_path = Path('Sprites', 'Crates', 'ammo-crate.png')
        super().__init__(image_path, pos, vel, angular_pos, angular_vel)
        return

    def do_action(self, spaceship: Spaceship) -> None:
        """
        Refill the spaceship's currently selected ammo to 100%.

        :param spaceship: The spaceship to refill ammo for.
        :type spaceship: Spaceship
        """
        spaceship.get_weapon().refill()
        return


class WeaponCrate(Crate):
    def __init__(
        self,
        pos,
        vel,
        angular_pos,
        angular_vel,
        weapon,
    ):
        super().__init__(
            weapon._item_image_path,
            pos,
            vel,
            angular_pos,
            angular_vel,
        )
        self.weapon = weapon
        return

    def do_action(self, spaceship: Spaceship):
        """
        Add the weapon to the spaceship's weapons array. If the weapon
        is already in the spaceship's weapons array, refill it.

        :param spaceship: The spaceship to add the weapon to.
        :type spaceship: Spaceship
        """
        # Get any weapon in the spaceship's weapons array that is of
        # the exact same type as the weapon in this crate. Does not
        # include subclasses.
        weapon_type_matches = [weapon for weapon in spaceship.weapons_array
                             if type(weapon) == type(self.weapon)]

        if len(weapon_type_matches) > 0:
            # Refill all weapons of matching type in the spaceship's
            # weapons array.
            for weapon in weapon_type_matches:
                weapon.refill()
        else:
            # If the weapon wasn't in the spaceship's weapons array,
            # add it.
            spaceship.weapons_array.append(self.weapon)

        return
