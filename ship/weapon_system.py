from collections.abc import Sequence

from pygame import Vector2

from projectiles import BaseProjectile
from weapons import BaseWeapon


class WeaponSystem:
    def __init__(
        self,
        pos: Vector2,
        weapons: Sequence[BaseWeapon],
    ) -> None:
        self._pos = pos
        self._weapons = list(weapons)
        self._weapon_i = 0
        return

    def get_weapon(self) -> BaseWeapon:
        """
        Return the currently selected weapon.

        :return: Currently selected weapon.
        :rtype: WeaponType
        """
        return self._weapons[self._weapon_i]

    def next_weapon(self) -> None:
        """
        Toggle to the next weapon.
        """
        # Increment the index counter by 1.
        self._shift_weapon_i(1)
        return

    def prev_weapon(self):
        """
        Toggle to the previous weapon.
        """
        # Decrement the index counter by 1.
        self._shift_weapon_i(-1)
        return

    def fire_weapon(
        self,
        base_pos: Vector2,
        base_vel: Vector2,
        base_angle: float,
    ) -> Sequence[BaseProjectile]:
        """
        Fire the spaceship's currently selected weapon.
        """
        new_projectiles = self.get_weapon().fire(
            # Offset the base position by the weapon system's position.
            base_pos + self._pos,
            base_vel,
            base_angle,
        )
        return new_projectiles

    def add_weapon(self, weapon: BaseWeapon) -> None:
        """
        Append the given weapon to the weapon system's array of
        weapons.

        :param weapon: Weapon to add to the list of weapons.
        :type weapon: BaseWeapon
        """
        self._weapons.append(weapon)
        return

    def _shift_weapon_i(self, n: int) -> None:
        """
        Increment the weapon index, wrapping the index around if it
        goes outside the valid index boundaries for the list of
        available weapons.
        """
        # print(self._weapon_i, end='->')
        self._weapon_i = (self._weapon_i + n) % self.weapons_count
        # print(self._weapon_i)
        return

    @property
    def weapons_count(self) -> int:
        return len(self._weapons)

    @property
    def pos(self) -> Vector2:
        return self._pos




# weapon_system = WeaponSystem(
#     Vector2(0, 0),
#     ['Weapon 1', 'Weapon 2', 'Weapon 3'],
# )
# assert weapon_system.get_weapon() == 'Weapon 1'

# weapon_system.next_weapon()
# assert weapon_system.get_weapon() == 'Weapon 2'

# weapon_system.next_weapon()
# assert weapon_system.get_weapon() == 'Weapon 3'

# weapon_system.prev_weapon()
# assert weapon_system.get_weapon() == 'Weapon 2'

# weapon_system.prev_weapon()
# assert weapon_system.get_weapon() == 'Weapon 1'

# weapon_system.next_weapon()
# weapon_system.next_weapon()
# weapon_system.next_weapon()
# assert weapon_system.get_weapon() == 'Weapon 1'

# weapon_system.prev_weapon()
# weapon_system.prev_weapon()
# weapon_system.prev_weapon()
# assert weapon_system.get_weapon() == 'Weapon 1'


# print(weapon_system.get_weapon())