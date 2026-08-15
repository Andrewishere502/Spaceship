import pygame

from settings_reader import get_path
from weapons import PhaseBlaster


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, pos, health):
        pygame.sprite.Sprite.__init__(self)
        self.base_pos = list(pos)

        sprite_image = get_path() / 'spaceship-2.png'

        self.base_image = pygame.image.load(sprite_image).convert_alpha()

        self.vel = [0, 0]  # in px/tick
        self.max_vel_component = 7

        self.angular_pos = 0  # in degrees

        self.max_health = health
        self.health = health

        self.weapons_array = [
            PhaseBlaster()
        ]
        self.weapon_index = 0
        self.score = 0
        self.asteriods_shot = 0
        return

    @property
    def is_alive(self):
        return bool(self.health)

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

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
        return

    def heal(self, health):
        self.health += health
        if self.health > self.max_health:
            self.health = self.max_health
        return

    def move(self):
        self.base_pos[0] += self.vel[0]
        self.base_pos[1] -= self.vel[1]
        return

    @property
    def weapon(self):
        return self.weapons_array[self.weapon_index]

    def next_weapon(self):
        self.weapon_index += 1
        if self.weapon_index >= len(self.weapons_array):
            self.weapon_index = 0
        return

    def prev_weapon(self):
        self.weapon_index -= 1
        if self.weapon_index < 0:
            self.weapon_index = len(self.weapons_array) - 1
        return

    def fire_weapon(self):
        return self.weapon.fire(self)
