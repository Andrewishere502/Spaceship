import pygame

from settings_reader import get_path


class Crate(pygame.sprite.Sprite):
    def __init__(self, image_name, pos, vel, angular_pos, angular_vel):
        pygame.sprite.Sprite.__init__(self)
        self.base_pos = list(pos)

        self.angular_pos = angular_pos  # in degrees
        self.angular_vel = angular_vel  # in degrees/tick

        self.vel = list(vel)  # in px/tick
        self.max_vel_component = 9

        self.image_name = image_name

        self.reload_base_image()
        return

    def reload_base_image(self):
        PATH = get_path()
        sprite_image = PATH + "Crates/" + self.image_name

        self.base_image = pygame.image.load(sprite_image)
        self.base_image.set_alpha()
        return

    @property
    def pos(self):
        """Return the position of the top left corner
        of the image
        """
        # This all corrects the position so the center
        # is always in the same place. Then the asteroid
        # doesn't look like its so wobbly.
        image = self.get_image()
        width_dif = image.get_width() - self.base_image.get_width()
        height_dif = image.get_height() - self.base_image.get_height()
        x_pos = int(self.base_pos[0] - width_dif / 2)
        y_pos = int(self.base_pos[1] - height_dif / 2)
        return (x_pos, y_pos)

    @property
    def center_pos(self):
        image = self.get_image()
        x_pos = int(self.pos[0] + image.get_width() / 2)
        y_pos = int(self.pos[1] + image.get_height() / 2)
        return (x_pos, y_pos)

    def get_image(self):
        image = pygame.transform.rotate(self.base_image, self.angular_pos)
        return image

    def get_hitbox(self):
        hb_width = self.base_image.get_width()
        hb_height = self.base_image.get_height()
        rect = pygame.Rect(*self.pos, hb_width, hb_height)
        rect.center = self.center_pos
        return rect

    def spin(self):
        self.angular_pos += self.angular_vel
        if self.angular_pos >= 360:
            self.angular_pos = self.angular_pos % 360
        return

    def move(self):
        self.base_pos[0] += self.vel[0]
        self.base_pos[1] -= self.vel[1]
        return

    def accelerate(self, acc):
        self.vel[0] += acc[0]
        if self.vel[0] > self.max_vel_component:
            self.vel[0] = self.max_vel_component
        elif self.vel[0] < -self.max_vel_component:
            self.vel[0] = -self.max_vel_component

        self.vel[1] += acc[1]
        if self.vel[1] > self.max_vel_component:
            self.vel[1] = self.max_vel_component
        elif self.vel[1] < -self.max_vel_component:
            self.vel[1] = -self.max_vel_component
        return


class HealthCrate(Crate):
    def __init__(self, pos, vel, angular_pos, angular_vel):
        image_name = "health-crate.png"
        super().__init__(image_name, pos, vel, angular_pos, angular_vel)
        return

    def do_action(self, spaceship):
        spaceship.heal(spaceship.max_health - spaceship.health)
        return


class AmmoCrate(Crate):
    def __init__(self, pos, vel, angular_pos, angular_vel):
        image_name = "ammo-crate.png"
        super().__init__(image_name, pos, vel, angular_pos, angular_vel)
        return

    def do_action(self, spaceship):
        refill_ammo = spaceship.weapon.max_ammo - spaceship.weapon.ammo
        spaceship.weapon.refill(refill_ammo)
        return


class WeaponCrate(Crate):
    def __init__(self, pos, vel, angular_pos, angular_vel, weapon):
        image_name = "weapon-crate.png"
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
