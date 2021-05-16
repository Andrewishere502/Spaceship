from math import sqrt, pi, cos, sin, acos

import pygame

from settings_reader import get_path


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, pos, size, vel, angular_pos, angular_vel):
        pygame.sprite.Sprite.__init__(self)
        self.base_pos = list(pos)

        self.angular_pos = angular_pos  # in degrees
        self.angular_vel = angular_vel  # in degrees/tick

        self.vel = list(vel)  # in px/tick
        self.max_vel_component = 9

        self.size = size

        self.reload_base_image()
        return

    def reload_base_image(self):
        PATH = get_path()
        sprite_image = PATH + "Asteroids/" + "asteroid-{}.png".format(self.size)

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

    @property
    def damage(self):
        return self.size * 3

    @property
    def point_value(self):
        return self.size * 50

    def split(self, damage):
        new_asteroid_mass = self.size - damage
        self.size -= damage

        vel_magnitude = sqrt(self.vel[0] ** 2 + self.vel[1] ** 2)
        vel_direction = acos(self.vel[0] / vel_magnitude)
        # acos always returns an angle pointed up (quadrant 1 or 2)
        # but this should only happen when the y component of velcoity
        # is positive. When y vel is negative, mirror the direction
        # across the x axis to point down.
        if self.vel[1] < 0:
            vel_direction = 2 * pi - vel_direction

        new_asteroid_vel_direction = vel_direction - pi / 6
        new_asteroid_x_vel = vel_magnitude * cos(new_asteroid_vel_direction)
        new_asteroid_y_vel = vel_magnitude * sin(new_asteroid_vel_direction)
        
        this_asteroid_vel_direction = vel_direction + pi / 6
        self.vel[0] = vel_magnitude * cos(this_asteroid_vel_direction)
        self.vel[1] = vel_magnitude * sin(this_asteroid_vel_direction)

        self.reload_base_image()

        new_asteroid = Asteroid(self.base_pos, new_asteroid_mass,
                                (new_asteroid_x_vel, new_asteroid_y_vel),
                                self.angular_pos, self.angular_vel)
        return new_asteroid