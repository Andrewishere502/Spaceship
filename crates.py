from pathlib import Path

from entity import Entity


class Crate(Entity):
    MAX_VEL_COMPONENT = 0.05
    MAX_AVEL = 0.5

    def __init__(
        self,
        image_name,
        initial_pos,
        initial_vel,
        initial_angle,
        initial_avel,
    ) -> None:
        image_path = Path('Sprites', 'Crates', image_name)
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
        image_name = 'health-crate.png'
        super().__init__(image_name, pos, vel, angular_pos, angular_vel)
        return

    def do_action(self, spaceship):
        spaceship.heal(spaceship.max_health - spaceship.health)
        return


class AmmoCrate(Crate):
    def __init__(self, pos, vel, angular_pos, angular_vel):
        image_name = 'ammo-crate.png'
        super().__init__(image_name, pos, vel, angular_pos, angular_vel)
        return

    def do_action(self, spaceship):
        refill_ammo = spaceship.weapon.max_ammo - spaceship.weapon.ammo
        spaceship.weapon.refill(refill_ammo)
        return


class WeaponCrate(Crate):
    def __init__(self, pos, vel, angular_pos, angular_vel, weapon):
        image_name = 'weapon-crate.png'
        super().__init__(image_name, pos, vel, angular_pos, angular_vel)
        self.weapon = weapon
        return

    def do_action(self, spaceship):
        # check to see if the weapon is repeated in weapons_array.
        weapon_repeated = False
        for weapon in spaceship.weapons_array:
            # if the weapon is in weapons_array already, refill it.
            if weapon.name == self.weapon.name:
                ammo = weapon.max_ammo - weapon.ammo
                weapon.refill(ammo)
                weapon_repeated = True
                break

        # if the weapon is not in weapons_array already, add it.
        if not weapon_repeated:
            spaceship.weapons_array.append(self.weapon)
        return
