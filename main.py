from pathlib import Path
import tomllib
import math

import pygame
from pygame import Vector2

from space import Space


class Display:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.win = pygame.display.set_mode((width, height))

        pygame.display.set_caption('Spaceship')
        return

    def clear(self):
        self.win.fill((0, 0, 0))
        return

    def blit(self, surf, pos):
        self.win.blit(surf, pos)
        return


def get_angle(point1: Vector2, point2: Vector2) -> float:
    """
    Return the angle between two points in degrees.
    """
    dx = point2.x - point1.x
    dy = point2.y - point1.y
    # Convert to degrees.
    angle = math.atan2(dy, dx) / math.pi * 180
    return angle


def mirror_y_axis(angle: float) -> float:
    """
    Return the given mangle mirrored across the y-axis.
    """
    angle *= -1
    angle += 180
    return angle


# Maximum frames per second
FPS = 60

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

SETTINGS_PATH = Path('settings.toml')

pygame.init()
pygame.font.init()

display = Display(SCREEN_WIDTH, SCREEN_HEIGHT)
clock = pygame.time.Clock()

# Initialize the space object with the user settings.
settings = tomllib.loads(SETTINGS_PATH.read_text())
space = Space(
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    **settings
)
space.reset_game()


pause = False
run = True
delta_ms = 0
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                space.reset_game()
            elif event.key == pygame.K_p:
                pause = not pause
            elif event.key == pygame.K_e:
                space.spaceship.next_weapon()
            elif event.key == pygame.K_q:
                space.spaceship.prev_weapon()
            elif event.key == pygame.K_SPACE:
                if space.spaceship.is_alive:
                    space.spaceship_shoot()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if space.spaceship.is_alive:
                buttons_down = pygame.mouse.get_pressed()
                if buttons_down[0]:
                    space.spaceship_shoot()

    # # Hold to shoot!
    # keys_pressed = pygame.key.get_pressed()
    # if keys_pressed[pygame.K_SPACE]:
    #     space.spaceship_shoot()

    display.clear()
    if space.spaceship.is_alive:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:  # move spaceship up
            space.spaceship.movement.apply_acceleration(Vector2(0, -0.005))
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:  # move spaceship down
            space.spaceship.movement.apply_acceleration(Vector2(0, 0.005))
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:  # move spaceship left
            space.spaceship.movement.apply_acceleration(Vector2(-0.005, 0))
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:  # move spaceship right
            space.spaceship.movement.apply_acceleration(Vector2(0.005, 0))

        if not pause:
            # Point the spaceship at the mouse.
            mouse_pos =  Vector2(*pygame.mouse.get_pos())
            new_spaceship_angle = get_angle(
                mouse_pos,
                space.spaceship.movement.get_pos(),
            )
            # Mirror the angle acros the y-axis because decreasing y
            # is up.
            new_spaceship_angle = mirror_y_axis(new_spaceship_angle)
            # Flip the spaceship's aim if the appropriate setting is
            # active.
            new_spaceship_angle += 180 * int(space._is_flip_aim)
            space.spaceship.movement.set_angle(new_spaceship_angle)

            space.step(delta_ms)

        space.clear()
        space.draw_all()

    display.blit(space, (0, 0))
    pygame.display.update()

    # Cap the frame rate to FPS frames per second. Frames can take longer
    # if the frame takes a long time to compute.
    # `delta_ms` is the number of milliseconds since the last frame was
    # rendered, allowing us to scale each step by time elapsed.
    delta_ms = clock.tick(FPS)
pygame.quit()
