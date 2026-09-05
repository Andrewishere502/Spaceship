import random
import math

import pygame
from pygame import Vector2

from entity import Entity
from asteroid import Asteroid
from spaceship import Spaceship
from projectiles import BaseProjectile
from weapons import (
    PhaseBlaster,
    PlasmaLauncher,
    IonFlak,
    AlloyCannon,
    IonRing
)
from crates import HealthCrate, AmmoCrate, WeaponCrate
from effects import Explosion


class Space(pygame.surface.Surface):
    def __init__(
        self,
        width: int,
        height: int,
        is_asteroids_do_damage: bool = True,
    ) -> None:
        super().__init__((width, height))

        self.font_big = pygame.font.SysFont('arial', 200)
        self.font_small = pygame.font.SysFont('arial', 50)

        self._is_asteroids_do_damage = is_asteroids_do_damage
        return

    def reset_game(
        self,
        spaceship: Spaceship
    ) -> None:
        """
        Reset the game.
        """
        self.level_tick_durration = 0
        self.level = 1
        self.ticks_until_asteroid = self.ticks_per_asteroid

        self.set_spaceship(spaceship)
        self.projectiles: list[BaseProjectile] = []

        self.asteroids: list[Asteroid] = []
        start_asteroids = 3
        for _ in range(start_asteroids):
            self.spawn_asteroid()

        self.crates: list[HealthCrate | AmmoCrate | WeaponCrate] = []

        self.effects = []
        return

    def set_spaceship(self, spaceship: Spaceship) -> None:
        self.spaceship = spaceship
        return

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
            self.spawn_crate(WeaponCrate)

        # spawn a crate every 2 levels.
        if self.level % 2 == 0:
            # give ammo to the player every 2 levels
            self.spawn_crate(AmmoCrate)

            # 2/3 chance to spawn a health crate
            do_spawn_health_crate = random.randint(0, 2)
            if do_spawn_health_crate:
                self.spawn_crate(HealthCrate)
        return

    ##
    # Display methods
    ##

    def draw_background(self):
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

    def draw_health_bar(self, padx: float, pady: float) -> None:
        HEALTH_BAR_WIDTH = 300
        HEALTH_BAR_HEIGHT = 10
        HEALTH_BAR_BASE_COLOR = (112, 112, 112)

        HEALTH_BAR_X = padx
        HEALTH_BAR_Y = self.get_height() - HEALTH_BAR_HEIGHT - pady

        # Draw the empty health bar so we can draw the health level
        # ontop of it.
        pygame.draw.rect(
            self,
            HEALTH_BAR_BASE_COLOR,
            (
                HEALTH_BAR_X,
                HEALTH_BAR_Y,
                HEALTH_BAR_WIDTH,
                HEALTH_BAR_HEIGHT,
            )
        )

        ship_hp_rate = self.spaceship.health.get_hp_ratio()
        if ship_hp_rate > 0.75:
            color = (14, 173, 0)
        elif ship_hp_rate > 0.50:
            color = (191, 201, 0)
        elif ship_hp_rate > 0.25:
            color = (209, 112, 0)
        else:
            color = (189, 3, 0)

        if ship_hp_rate > 0:
            pygame.draw.rect(
                self,
                color,
                (
                    HEALTH_BAR_X,
                    HEALTH_BAR_Y,
                    HEALTH_BAR_WIDTH * ship_hp_rate,
                    HEALTH_BAR_HEIGHT,
                )
            )
        return

    def draw_level_progress(self):
        LEVEL_BAR_WIDTH = self.get_width()
        LEVEL_BAR_HEIGHT = 5
        LEVEL_BAR_BASE_COLOR = (112, 112, 112)
        LEVEL_BAR_TOP_COLOR = (219, 219, 219)

        pygame.draw.rect(
            self,
            LEVEL_BAR_BASE_COLOR,
            (
                0,
                0,
                LEVEL_BAR_WIDTH,
                LEVEL_BAR_HEIGHT,
            )
        )

        level_progress_ratio = self.level_tick_durration / self.ticks_per_level
        if level_progress_ratio > 0:
            pygame.draw.rect(
                self,
                LEVEL_BAR_TOP_COLOR,
                (
                    0,
                    0,
                    LEVEL_BAR_WIDTH * level_progress_ratio,
                    LEVEL_BAR_HEIGHT,
                )
            )
        return

    def draw_weapon(self, padx: float, pady: int):
        AMMO_BAR_COLOR = (227, 189, 0)
        AMMO_BAR_HEIGHT = 10

        # Draw the image of the weapon on the screen.
        weapon_image = self.spaceship.get_weapon().image
        weapon_width, weapon_height = weapon_image.get_rect().size
        weapon_x = self.get_width() - weapon_width - padx
        weapon_y = self.get_height() - weapon_height - pady
        self.blit(weapon_image, (weapon_x, weapon_y - AMMO_BAR_HEIGHT))

        # Only draw the ammo bar if there is some ammo remaining.
        ammo_percent = self.spaceship.get_weapon().get_ammo_ratio()
        if ammo_percent > 0:
            pygame.draw.rect(
                self,
                AMMO_BAR_COLOR,
                (
                    weapon_x,
                    self.get_height() - AMMO_BAR_HEIGHT - pady,
                    weapon_width * ammo_percent,
                    AMMO_BAR_HEIGHT,
                )
            )
        return

    def draw_overlay(self):
        OVERLAY_PADX = 10
        OVERLAY_PADY = 10

        self.draw_weapon(
            OVERLAY_PADX,
            OVERLAY_PADY,
        )

        text = str(self.level)
        pos = self.text_to_center_point(text, self.font_big, (self.get_width() // 2, self.get_height() // 2))
        self.write_big(text, (72, 66, 84), pos)

        self.draw_health_bar(
            OVERLAY_PADX,
            OVERLAY_PADY,
        )

        self.draw_level_progress()

        text = 'Score: ' + str(self.spaceship.score)
        pos = self.text_to_center_point(text, self.font_small, (self.get_width() // 2, self.get_height() // 2 + 100))
        self.write_small(text, (20, 110, 8), pos)
        return

    def draw_entity(self, entity: Entity) -> None:
        image = entity.get_image()
        rect = entity.get_image().get_rect(center=entity.movement.get_pos())
        self.blit(image, rect)
        return

    def draw_effects(self):
        for effect in self.effects:
            self.blit(effect.get_frame(), effect.pos)
        return

    def draw_all(self):
        self.draw_background()

        self.draw_overlay()

        for crate in self.crates:
            self.draw_entity(crate)

        for asteroid in self.asteroids:
            self.draw_entity(asteroid)

        if self.spaceship.is_alive:
            self.draw_entity(self.spaceship)

        for projectile in self.projectiles:
            self.draw_entity(projectile)

        self.draw_effects()
        return

    # def draw_rect

    ##
    # Misc methods
    ##

    def step(self, delta_ms: int):
        asteroid_hitboxes = [asteroid.get_hitbox() for asteroid in self.asteroids]
        crate_hitboxes = [crate.get_hitbox() for crate in self.crates]

        # control spaceship!
        if self.spaceship.is_alive:
            self.spaceship.movement.step(delta_ms)

            # Wrap the spaceship around to the other side of the
            # screen.
            pos = self.spaceship.movement.get_pos()
            self.spaceship.movement.set_pos(
                Vector2(
                    pos.x % self.get_width(),
                    pos.y % self.get_height(),
                )
            )

            # test if the spaceship got hit by an asteroid
            collide_i = self.spaceship.get_hitbox().collidelist(asteroid_hitboxes)
            if collide_i > -1:
                asteroid = self.asteroids[collide_i]

                if self._is_asteroids_do_damage:
                    self.spaceship.health.adjust_hitpoints(-asteroid.damage)

                # test if the spaceship died
                if not self.spaceship.is_alive:
                    self.add_explosion(self.spaceship.movement.get_pos(), 1.5)
                else:
                    self.add_explosion(asteroid.movement.get_pos(), 1)

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
        for asteroid in self.asteroids:
            asteroid.movement.step(delta_ms)
            pos = asteroid.movement.get_pos()
            # Wrap the asteroid around the other side of the screen.
            asteroid.movement.set_pos(
                Vector2(
                    pos.x % self.get_width(),
                    pos.y % self.get_height(),
                )
            )

        # control crates
        for crate in self.crates:
            crate.movement.step(delta_ms)
            pos = crate.movement.get_pos()
            # Wrap the asteroid around the other side of the screen.
            crate.movement.set_pos(
                Vector2(
                    pos.x % self.get_width(),
                    pos.y % self.get_height(),
                )
            )

        # control projectiles
        i = 0
        while len(self.projectiles):
            increment_i = True
            projectile = self.projectiles[i]

            pos = projectile.movement.get_pos()
            # Wrap the asteroid around the other side of the screen.
            projectile.movement.set_pos(
                Vector2(
                    pos.x % self.get_width(),
                    pos.y % self.get_height(),
                )
            )

            if not projectile.get_is_done():
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
                    projectile.step(delta_ms)
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

    ##
    # Spaceship methods
    ##

    def spaceship_shoot(self) -> None:
        self.projectiles.extend(self.spaceship.fire_weapon())
        return

    ##
    # Asteroid methods
    ##

    def spawn_asteroid(self):
        # Maximum magnitude of velocity is 0.1.
        MAX_SPEED = 0.1

        # Spawn on either the left or right side.
        rand_x = random.choice((0, self.get_width()))
        # Span at any height value.
        rand_y = random.randint(0, self.get_height())

        angle = random.randint(0, 359)
        speed = random.random() * MAX_SPEED
        initial_vel = Vector2(
            math.sqrt(speed),
            math.sqrt(speed),
        ).rotate(
            angle
        )

        size = random.randint(2, 3)

        asteriod = Asteroid(
            Vector2(rand_x, rand_y),
            initial_vel,
            angle,
            (random.random() - 0.5),  # -0.5 to 0.5
            size,
        )
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

    def spawn_crate(self, crate_type: type[HealthCrate | AmmoCrate | WeaponCrate]) -> None:
        # Spawn on either the left or right side.
        rand_x = random.choice((0, self.get_width()))
        # Span at any height value.
        rand_y = random.randint(0, self.get_height())

        angle = random.randint(0, 359)
        speed = random.random() * (crate_type.MAX_VEL_COMPONENT ** 2)
        initial_vel = Vector2(
            math.sqrt(speed),
            math.sqrt(speed),
        ).rotate(
            angle
        )

        # Angular velocity in degrees.
        initial_avel = (random.random() - 0.5) * 2 * crate_type.MAX_AVEL

        crate_args = (
            Vector2(rand_x, rand_y),
            initial_vel,
            angle,
            initial_avel,
        )
        if crate_type == HealthCrate:
            crate = self.make_health_crate(*crate_args)
        elif crate_type == AmmoCrate:
            crate = self.make_ammo_crate(*crate_args)
        elif crate_type == WeaponCrate:
            crate = self.make_weapon_crate(*crate_args)
        else:
            raise TypeError(
                f'Unknown crate type {crate_type!r}'
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
                            set(self.spaceship.weapon_system._weapons)
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
