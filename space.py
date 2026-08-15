import random
from math import pi, sin, cos, atan

import pygame

from asteroid import Asteroid
from spaceship import Spaceship
from weapons import (PhaseBlaster, PlasmaLauncher, IonFlak,
                     AlloyCannon, IonRing)
from crates import HealthCrate, AmmoCrate, WeaponCrate
from effects import Explosion
from settings_reader import get_settings


class Space(pygame.surface.Surface):
    def __init__(self, width, height):
        pygame.surface.Surface.__init__(self, (width, height))
        self.width = width
        self.height = height
        self.font_big = pygame.font.SysFont('arial', 200)
        self.font_small = pygame.font.SysFont('arial', 50)
        return

    def reset_game(self):
        self.settings = get_settings()
        
        self.level_tick_durration = 0
        self.level = 1
        self.ticks_until_asteroid = self.ticks_per_asteroid

        self.spaceship = Spaceship((self.width // 2, self.height // 2), 10)
        self.projectiles = []

        self.asteroids = []
        start_asteroids = 3
        for _ in range(start_asteroids):
            self.spawn_asteroid()

        self.crates = []

        self.effects = []

        self.clear()
        return

    def check_setting(self, name, default):
        return self.settings.get(name, default)

    ##
    # Level methods
    ##

    @property
    def asteroids_per_level(self):
        """Return an integer that represents the number of additional
        asteroids the game should spawn each level.
        """
        m = 1.2  # the increase in asteroids per level per level
        b = 2  # asteroids on the first level
        return round(m * (self.level - 1) + b)

    @property
    def ticks_per_asteroid(self):
        base_ticks_per_asteroid = 70
        if self.level <= 10:
            return base_ticks_per_asteroid
        else:
            return base_ticks_per_asteroid - self.level + 10

    @property
    def ticks_per_level(self):
        return self.asteroids_per_level * self.ticks_per_asteroid

    def increment_tick(self):
        self.level_tick_durration += 1
        if self.level_tick_durration >= self.ticks_per_level:
            self.next_level()

        self.ticks_until_asteroid -= 1
        if self.ticks_until_asteroid == 0:
            self.spawn_asteroid()
            self.ticks_until_asteroid = self.ticks_per_asteroid
        return

    def next_level(self):
        self.level += 1
        self.level_tick_durration = 1
        
        # 1/7 chance to spawn weapon crate
        do_spawn_weapon_crate = not random.randint(0, 6)
        if do_spawn_weapon_crate:
            self.spawn_crate("weapon")

        # spawn a crate every 2 levels.
        if self.level % 2 == 0:
            # give ammo to the player every 2 levels
            self.spawn_crate("ammo")

            # 2/3 chance to spawn a health crate
            do_spawn_health_crate = random.randint(0, 2)
            if do_spawn_health_crate:
                self.spawn_crate("health")
        return

    ##
    # Display methods
    ##

    def clear(self):
        self.fill((5, 0, 20))
        # self.fill((100, 100, 100))  # for higher contrast
        return

    def write_big(self, text, color, pos):
        text_render = self.font_big.render(text, True, color)
        self.blit(text_render, pos)
        return

    def write_small(self, text, color, pos):
        text_render = self.font_small.render(text, True, color)
        self.blit(text_render, pos)
        return

    def text_to_center_point(self, text, font, pos):
        text_width, text_height = font.size(text)

        x_pos = pos[0] - text_width // 2
        y_pos = pos[1] - text_height // 2
        return (x_pos, y_pos)

    def draw_health_bar(self):
        health_bar_width = 300
        health_bar_height = 10
        health_bar = pygame.surface.Surface((health_bar_width, health_bar_height))
        ship_percent_health = self.spaceship.health / self.spaceship.max_health
        if ship_percent_health > 0.85:
            color = (84, 186, 0)
        elif ship_percent_health > 0.70:
            color = (186, 186, 0)
        elif ship_percent_health > 0.50:
            color = (186, 118, 0)
        elif ship_percent_health > 0.20:
            color = (186, 71, 0)
        else:
            color = (186, 12, 0)
        pygame.draw.rect(health_bar, (112, 112, 112), (0, 0, health_bar_width, health_bar_height))
        color_x_pos = health_bar.get_width() // 2 - health_bar_width * ship_percent_health // 2
        if ship_percent_health > 0:
            pygame.draw.rect(health_bar, color, (color_x_pos, 0, health_bar_width * ship_percent_health, health_bar_height))
        health_bar.set_alpha(150)

        bar_x_pos = self.width // 2 - health_bar_width // 2
        bar_y_pos = self.height - 20
        self.blit(health_bar, (bar_x_pos, bar_y_pos))
        return

    def draw_level_progress(self):
        level_bar_width = self.width
        level_bar_height = 5
        level_bar = pygame.surface.Surface((level_bar_width, level_bar_height))
        level_progress = self.level_tick_durration / self.ticks_per_level
        pygame.draw.rect(level_bar, (112, 112, 112), (0, 0, level_bar_width, level_bar_height))
        if level_progress > 0:
            pygame.draw.rect(level_bar, (219, 219, 219), (0, 0, level_bar_width * level_progress, level_bar_height))
        level_bar.set_alpha(150)
        self.blit(level_bar, (0, 0))
        return

    def draw_weapon(self):
        weapon_bar_x = 462
        weapon_bar_y = 513

        ammo_bar_y = 580
        ammo_bar_width = 128

        if hasattr(self.spaceship.weapon, "image"):
            weapon_image = self.spaceship.weapon.image
            # weapon_image.convert_alpha()

            # blit the image of the weapon to the screen
            self.blit(weapon_image, (weapon_bar_x, weapon_bar_y))
        
        ammo_percent = self.spaceship.weapon.ammo / self.spaceship.weapon.max_ammo

        if ammo_percent > 0:
            pygame.draw.rect(self, (227, 189, 0), (weapon_bar_x, ammo_bar_y, ammo_bar_width * ammo_percent, 10))

        return

    def draw_overlay(self):
        text = str(self.level)
        pos = self.text_to_center_point(text, self.font_big, (self.width // 2, self.height // 2))
        self.write_big(text, (72, 66, 84), pos)

        self.draw_weapon()

        self.draw_health_bar()

        self.draw_level_progress()

        text = "Score: " + str(self.spaceship.score)
        pos = self.text_to_center_point(text, self.font_small, (self.width // 2, self.height // 2 + 100))
        self.write_small(text, (20, 110, 8), pos)
        return

    def draw_asteroids(self):
        # blit asteroids
        for asteroid in self.asteroids:
            self.blit(asteroid.get_image(), asteroid.pos)
        return

    def draw_spaceship(self):
        # blit spaceship
        self.blit(self.spaceship.get_image(), self.spaceship.pos)
        return

    def draw_projectiles(self):
        # blit projectiles
        for projectile in self.projectiles:
            self.blit(projectile.image, projectile.pos)
        return

    def draw_crates(self):
        # blit crates
        for crate in self.crates:
            self.blit(crate.get_image(), crate.pos)
        return

    def draw_effects(self):
        for effect in self.effects:
            self.blit(effect.get_frame(), effect.pos)
        return

    def draw_all(self):
        self.draw_overlay()
        self.draw_crates()
        self.draw_asteroids()
        self.draw_projectiles()
        if self.spaceship.is_alive:
            self.draw_spaceship()
        self.draw_effects()
        return

    ##
    # Misc methods
    ##

    def randomize_pos(self, pos):
        return tuple(map(lambda c: c + random.randint(34, 45) * random.choice((-1, 1)), pos))

    def tick(self):
        asteroid_hitboxes = [asteroid.get_hitbox() for asteroid in self.asteroids]
        crate_hitboxes = [crate.get_hitbox() for crate in self.crates]

        # control spaceship!
        if self.spaceship.is_alive:
            self.spaceship.move()
            self.loop_thing(self.spaceship)
            
            # test if the spaceship got hit by an asteroid
            collide_i = self.spaceship.get_hitbox().collidelist(asteroid_hitboxes)
            if collide_i > -1:
                asteroid = self.asteroids[collide_i]

                if self.check_setting("asteroids_do_damage", 1):
                    self.spaceship.take_damage(asteroid.damage)

                # test if the spaceship died
                if not self.spaceship.is_alive:
                    self.add_explosion(self.spaceship.center_pos, 1.5)
                else:
                    self.add_explosion(asteroid.center_pos, 1)

                # delete the asteroid from asteroid_hitboxes
                # *and* self.asteroids so asteroid_hitboxes doesn't
                # have to be recalculated
                asteroid_hitboxes.pop(collide_i)
                self.asteroids.pop(collide_i)
            
            # test if the spaceship picked up a crate
            collide_i = self.spaceship.get_hitbox().collidelist(crate_hitboxes)
            if collide_i > -1:
                crate = self.crates[collide_i]

                crate.do_action(self.spaceship)

                # delete the crate from crate_hitboxes
                # *and* self.crates so crate_hitboxes doesn't
                # have to be recalculated
                crate_hitboxes.pop(collide_i)
                self.crates.pop(collide_i)

        # control asteroids
        i = 0
        while len(self.asteroids):
            increment_i = True
            asteroid = self.asteroids[i]

            asteroid.move()
            asteroid.spin()
            self.loop_thing(asteroid)

            if self.check_setting("combine_asteroids", 0):
                collide_i = asteroid.get_hitbox().collidelist(asteroid_hitboxes)
                # collides with asteroid thats not itself
                if collide_i > -1 and collide_i != i:
                    collide_asteroid = self.asteroids[collide_i]

                    # The following code determines if the asteroids
                    # are actually moving into each other or not. This
                    # is important because we don't want to combine
                    # asteroids that have just been split and are now
                    # moving away from each other.
                    #
                    # dx and dx_vel are positive when asteroid is to
                    # the right of collide_asteroid, and negative when it
                    # is to the left
                    dx = round(asteroid.center_pos[0] - collide_asteroid.center_pos[0], 6)
                    dx_vel = round(asteroid.vel[0] - collide_asteroid.vel[0], 6)
                    try:
                        x_collide = dx / dx_vel < 0
                    except ZeroDivisionError:
                        x_collide = False

                    # dy and dy_vel are positive when asteroid above
                    # collide_asteroid, and negative when it is below
                    dy = round(collide_asteroid.center_pos[1] - asteroid.center_pos[1], 6)
                    dy_vel = round(asteroid.vel[1] - collide_asteroid.vel[1], 6)
                    try:
                        y_collide = dy / dy_vel < 0
                    except ZeroDivisionError:
                        y_collide = False

                    if x_collide or y_collide:
                        if asteroid.size > collide_asteroid.size:
                            # this asteroid consumes the other one
                            self.merge_asteroids(asteroid, collide_asteroid)
                            # delete the asteroid from asteroid_hitboxes
                            # *and* self.asteroids so asteroid_hitboxes doesn't
                            # have to be recalculated
                            asteroid_hitboxes.pop(collide_i)
                            self.asteroids.pop(collide_i)
                            if i > collide_i:
                                increment_i = False
                        else:
                            # the other asteroid consumes this one
                            self.merge_asteroids(collide_asteroid, asteroid)
                            # delete the asteroid from asteroid_hitboxes
                            # *and* self.asteroids so asteroid_hitboxes doesn't
                            # have to be recalculated
                            asteroid_hitboxes.pop(i)
                            self.asteroids.pop(i)
                            increment_i = False

            if increment_i:
                i += 1

            if i == len(self.asteroids):
                break

        # control crates
        for crate in self.crates:
            crate.move()
            crate.spin()
            self.loop_thing(crate)

        # control projectiles
        i = 0
        while len(self.projectiles):
            increment_i = True
            projectile = self.projectiles[i]
            
            self.loop_thing(projectile)
            if not projectile.dead:  # projectile is still 'alive'
                collide_i = projectile.get_hitbox().collidelist(asteroid_hitboxes)
                if collide_i > -1:  # projectile hit an asteroid
                    asteroid_point_val = self.asteroids[collide_i].point_value
                    if self.asteroids[collide_i].size <= projectile.damage:
                        asteroid_hitboxes.pop(collide_i)
                        self.asteroids.pop(collide_i)
                    else:
                        new_asteroid = self.asteroids[collide_i].split(projectile.damage)
                        asteroid_hitboxes.append(new_asteroid.get_hitbox())
                        asteroid_hitboxes = [asteroid.get_hitbox() for asteroid in self.asteroids]
                        self.asteroids.append(new_asteroid)
                    self.spaceship.asteriods_shot += 1
                    self.spaceship.score += asteroid_point_val
                    self.projectiles.pop(i)
                    increment_i = False
                else:  # projectile did not hit an asteroid
                    projectile.move()
            else:  # projectile has died and must be removed
                self.projectiles.pop(i)
                increment_i = False

            if increment_i:
                i += 1

            if i == len(self.projectiles):
                break

        # control effects
        i = 0
        while len(self.effects):
            effect = self.effects[i]

            effect.tick()

            if effect.done:
                self.effects.pop(i)
            else:
                i += 1

            if i == len(self.effects):
                break

        self.increment_tick()
        return

    def loop_thing(self, thing):
        """Loop a thing to the other side of the screen
        when it goes out of bounds
        """
        try:
            image = thing.get_image()
        except AttributeError:
            image = thing.image

        # loop the thing's x position
        did_x_loop = False
        x_padding = image.get_width() * 0.2
        if thing.center_pos[0] < 0 - x_padding:
            thing.base_pos[0] = int(self.width - image.get_width() / 2)
            did_x_loop = True
        elif thing.center_pos[0] > self.width + x_padding:
            thing.base_pos[0] = int(0 - image.get_width() / 2)
            did_x_loop = True

        if (isinstance(thing, Asteroid)
            and self.check_setting("speed_up_when_loop", 0)):
            if did_x_loop:
                if thing.vel[0] < 0:
                    thing.accelerate((-1, 0))
                else:
                    thing.accelerate((1, 0))

        # loop the thing's y position
        did_y_loop = False
        y_padding = image.get_width() * 0.2
        if thing.center_pos[1] < 0 - y_padding:
            thing.base_pos[1] = int(self.height - image.get_height() / 2)
            did_y_loop = True
        elif thing.center_pos[1] > self.height + y_padding:
            thing.base_pos[1] = int(0 - image.get_height() / 2)
            did_y_loop = True

        if (isinstance(thing, Asteroid)
            and self.check_setting("speed_up_when_loop", 0)):
            if did_y_loop:
                if thing.vel[1] < 0:
                    thing.accelerate((0, -1))
                else:
                    thing.accelerate((0, 1))
        return

    ##
    # Spaceship methods
    ##

    def point_spaceship(self, pos):
        x_dis = abs(pos[0] - self.spaceship.center_pos[0])
        y_dis = abs(pos[1] - self.spaceship.center_pos[1])
        try:
            angle = atan(y_dis / x_dis) / pi * 180

            if pos[0] < self.spaceship.center_pos[0]:
                # reflect accross y axis
                angle = 180 - angle

            if pos[1] > self.spaceship.center_pos[1]:
                # reflect accross x axis
                angle = 360 - angle

        except ZeroDivisionError:
            if pos[1] < self.spaceship.center_pos[1]:
                angle = 90
            else:
                angle = 270

        if self.check_setting("flip_aim", 0):
            angle += 180
        
        self.spaceship.angular_pos = angle
        return

    def spaceship_shoot(self):
        projectiles = self.spaceship.fire_weapon()
        if projectiles == None:
            return
        elif isinstance(projectiles, (list, tuple)):
            # projectiles is multiple projectiles
            self.projectiles.extend(projectiles)
        else:
            # projectiles is just one projectile
            self.projectiles.append(projectiles)
        return

    ##
    # Asteroid methods
    ##

    def spawn_asteroid(self):
        rand_x = random.choice((0, self.width))
        rand_y = random.randint(0, self.height)

        size = random.randint(2, 3)

        vel = random.randint(3, 5)
        quadrant = random.randint(1, 4)
        if quadrant == 1:
            direction = random.randint(20, 70)
        elif quadrant == 2:
            direction = random.randint(110, 160)
        elif quadrant == 3:
            direction = random.randint(200, 250)
        else:  # in quadrant 4
            direction = random.randint(290, 340)
        direction = direction / 180 * pi
        x_vel = vel * cos(direction)
        y_vel = vel * sin(direction)

        angular_pos = random.randint(0, 359)  # in degrees
        angular_vel = random.randint(-5, 5)  # in degrees/tick
    
        asteriod = Asteroid((rand_x, rand_y), size, (x_vel, y_vel), angular_pos, angular_vel)
        self.asteroids.append(asteriod)
        return

    def merge_asteroids(self, asteroid1, asteroid2):
        asteroid1.accelerate(tuple(map(lambda c: c * 0.2, asteroid2.vel)))
        
        asteroid1.size += asteroid2.size
        if asteroid1.size > 5:
            asteroid1.size = 5

        asteroid1.reload_base_image()
        return

    ##
    # Power up methods
    ##

    def spawn_random_crate(self, crates):
        rand_x = random.choice((0, self.width))
        rand_y = random.randint(0, self.height)

        vel = random.randint(3, 5)
        # choose the quadrant the angle will be in
        quadrant = random.randint(1, 4)
        if quadrant == 1:
            direction = random.randint(20, 70)
        elif quadrant == 2:
            direction = random.randint(110, 160)
        elif quadrant == 3:
            direction = random.randint(200, 250)
        else:  # in quadrant 4
            direction = random.randint(290, 340)
        direction = direction / 180 * pi
        x_vel = vel * cos(direction)
        y_vel = vel * sin(direction)

        angular_pos = random.randint(0, 359)  # in degrees
        angular_vel = random.randint(-5, 5)  # in degrees/tick

        crate_type = random.choice(crates)
        crate_maker = getattr(self, "make_" + crate_type + "_crate")
        crate = crate_maker((rand_x, rand_y),
                            (x_vel, y_vel),
                            angular_pos,
                            angular_vel
                            )

        self.crates.append(crate)
        return

    def spawn_crate(self, crate_type):
        rand_x = random.choice((0, self.width))
        rand_y = random.randint(0, self.height)

        vel = random.randint(3, 5)
        # choose the quadrant the angle will be in
        quadrant = random.randint(1, 4)
        if quadrant == 1:
            direction = random.randint(20, 70)
        elif quadrant == 2:
            direction = random.randint(110, 160)
        elif quadrant == 3:
            direction = random.randint(200, 250)
        else:  # in quadrant 4
            direction = random.randint(290, 340)
        direction = direction / 180 * pi
        x_vel = vel * cos(direction)
        y_vel = vel * sin(direction)

        angular_pos = random.randint(0, 359)  # in degrees
        angular_vel = random.randint(-5, 5)  # in degrees/tick

        crate_maker = getattr(self, "make_" + crate_type + "_crate")
        crate = crate_maker((rand_x, rand_y),
                            (x_vel, y_vel),
                            angular_pos,
                            angular_vel
                            )

        self.crates.append(crate)
        return

    def make_health_crate(self, pos, vel, angular_pos, angular_vel):
        crate = HealthCrate(pos, vel, angular_pos, angular_vel)
        return crate

    def make_ammo_crate(self, pos, vel, angular_pos, angular_vel):
        crate = AmmoCrate(pos, vel, angular_pos, angular_vel)
        return crate

    def make_weapon_crate(self, pos, vel, angular_pos, angular_vel):
        """Return a weapon crate that contains a weapon that the user
        doesn't have.
        """
        weapons = set([PhaseBlaster(),
                       PlasmaLauncher(),
                       IonFlak(),
                       AlloyCannon(),
                       IonRing()
                       ])
        weapon_choices = list(weapons.difference(
                            set(self.spaceship.weapons_array)
                            ))
        weapon = random.choice(weapon_choices)
        crate = WeaponCrate(pos, vel, angular_pos, angular_vel, weapon)
        return crate

    ##
    # Effect methods
    ##

    def add_effect(self, effect):
        self.effects.append(effect)
        return

    def add_explosion(self, center_pos, scale):
        explosion = Explosion((0,0), scale)
        explosion.set_center(center_pos)
        self.add_effect(explosion)
        return
