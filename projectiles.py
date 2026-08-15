import pygame
from math import pi, cos, sin

from settings_reader import get_path


class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, image, vel, damage, angular_pos, tick_life):
        pygame.sprite.Sprite.__init__(self)
        self.base_pos = list(pos)

        sprite_image = get_path() / 'Projectiles' / image

        base_image = pygame.image.load(sprite_image).convert_alpha()
        self.base_width = base_image.get_width()
        self.base_height = base_image.get_height()
        self.image = pygame.transform.rotate(base_image, angular_pos)
        
        self.vel = list(vel)  # in px/tick
        
        self.damage = damage  # sizes to decrease asteroid by

        self.tick_life = tick_life
        return

    @property
    def pos(self):
        '''Return the position of the top left corner
        of the image
        '''
        # This all corrects the position so the center
        # is always in the same place. Then the asteroid
        # doesn't look like its so wobbly.
        image = self.image
        width_dif = image.get_width() - self.base_width
        height_dif = image.get_height() - self.base_height
        x_pos = int(self.base_pos[0] - width_dif / 2)
        y_pos = int(self.base_pos[1] - height_dif / 2)
        return (x_pos, y_pos)

    @property
    def center_pos(self):
        x_pos = int(self.pos[0] + self.image.get_width() / 2)
        y_pos = int(self.pos[1] + self.image.get_height() / 2)
        return (x_pos, y_pos)

    def get_hitbox(self):
        rect = pygame.Rect(*self.pos, self.base_width, self.base_height)
        rect.center = self.center_pos
        return rect

    @property
    def dead(self):
        return self.tick_life <= 0

    def move(self):
        self.base_pos[0] += self.vel[0]
        self.base_pos[1] -= self.vel[1]

        self.tick_life -= 1
        return

    def set_center(self, center_pos):
        width = self.image.get_width()
        height = self.image.get_height()
        self.base_pos[0] = center_pos[0] - width // 2
        self.base_pos[1] = center_pos[1] - height // 2
        return


class PhaserProjectile(Projectile):
    def __init__(self, pos, angular_pos):
        vel_magnitude = 10
        x_vel = vel_magnitude * cos((angular_pos) / 180 * pi)
        y_vel = vel_magnitude * sin((angular_pos) / 180 * pi)
        vel_components = [x_vel, y_vel]

        damage = 1
        tick_life = 40
        
        super().__init__(pos, 'phaser-projectile.png',
                         vel_components, damage,
                         angular_pos, tick_life)
        return


class PlasmaProjectile(Projectile):
    def __init__(self, pos, angular_pos):
        vel_magnitude = 8
        x_vel = vel_magnitude * cos((angular_pos) / 180 * pi)
        y_vel = vel_magnitude * sin((angular_pos) / 180 * pi)
        vel_components = [x_vel, y_vel]

        damage = 2
        tick_life = 40
        
        super().__init__(pos, 'plasma-projectile.png',
                         vel_components, damage,
                         angular_pos, tick_life)
        return


class IonProjectile(Projectile):
    def __init__(self, pos, angular_pos):
        vel_magnitude = 13
        x_vel = vel_magnitude * cos((angular_pos) / 180 * pi)
        y_vel = vel_magnitude * sin((angular_pos) / 180 * pi)
        vel_components = [x_vel, y_vel]

        damage = 1
        tick_life = 10
        
        super().__init__(pos, 'ion-projectile.png',
                         vel_components, damage,
                         angular_pos, tick_life)
        return

class AlloyProjectile(Projectile):
    def __init__(self, pos, angular_pos):
        vel_magnitude = 8
        x_vel = vel_magnitude * cos((angular_pos) / 180 * pi)
        y_vel = vel_magnitude * sin((angular_pos) / 180 * pi)
        vel_components = [x_vel, y_vel]

        damage = 1
        tick_life = 60
        
        super().__init__(pos, 'alloy-projectile.png',
                         vel_components, damage,
                         angular_pos, tick_life)
        return
