from pathlib import Path
import tomllib
from functools import partial
from collections.abc import Callable

import pygame
from pygame import Vector2

from space import Space
from spaceship import Spaceship
from controllers import (
    InputController,
)


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


def get_keyboard_mapping(
    space: Space,
    spaceship: Spaceship
) -> dict[int, Callable]:
    """

    """
    INPUT_MAPPING = {
        pygame.K_SPACE: space.spaceship_shoot,

        # Arrow key movement mappings.
        pygame.K_UP: partial(
            spaceship.movement.apply_acceleration,
            Vector2(0, -0.005)
        ),
        pygame.K_DOWN: partial(
            spaceship.movement.apply_acceleration,
            Vector2(0, 0.005)
        ),
        pygame.K_LEFT: partial(
            spaceship.movement.apply_acceleration,
            Vector2(-0.005, 0)
        ),
        pygame.K_RIGHT: partial(
            spaceship.movement.apply_acceleration,
            Vector2(0.005, 0)
        ),

        # WASD key movement mappings.
        pygame.K_w: partial(  # Up
            spaceship.movement.apply_acceleration,
            Vector2(0, -0.005)
        ),
        pygame.K_a: partial(  # Left
            spaceship.movement.apply_acceleration,
            Vector2(-0.005, 0)
        ),
        pygame.K_s: partial(  # Down
            spaceship.movement.apply_acceleration,
            Vector2(0, 0.005)
        ),
        pygame.K_d: partial(  # Right
            spaceship.movement.apply_acceleration,
            Vector2(0.005, 0)
        ),
    }
    return INPUT_MAPPING


def make_spaceship(
    initial_pos: Vector2,
) -> Spaceship:
    """
    Return a new spaceship instance.
    """
    spaceship = Spaceship(
        initial_pos,
        10,
    )
    return spaceship


# Maximum frames per second.
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

# Reset the game with the spaceship.
spaceship = make_spaceship(
    Vector2(space.get_rect().center),
)
space.reset_game(spaceship)

# Setup the spaceship controller.
controller = InputController()
controller.set_map(
    get_keyboard_mapping(
        space,
        spaceship,
    )
)

pause = False
run = True
delta_ms = 0
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                spaceship = make_spaceship(
                    Vector2(space.get_rect().center),
                )
                space.reset_game(spaceship)
                controller.set_map(
                    get_keyboard_mapping(
                        space,
                        spaceship,
                    )
                )
            elif event.key == pygame.K_e:
                spaceship.next_weapon()
            elif event.key == pygame.K_q:
                spaceship.prev_weapon()
            elif event.key == pygame.K_p:
                pause = not pause
            else:
                controller.send(event.key)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if space.spaceship.is_alive:
                buttons_down = pygame.mouse.get_pressed()
                if buttons_down[0]:
                    space.spaceship_shoot()

    if spaceship.is_alive and not pause:
        keys_pressed = pygame.key.get_pressed()
        # For each mapped input, send it to the controller if it's
        # down (pressed).
        for key in set(controller._input_map.keys()):
            is_down = keys_pressed[key]
            if is_down:
                controller.send(key)

        # Point the spaceship at the mouse.
        mouse_pos = Vector2(*pygame.mouse.get_pos())
        spaceship.movement.point_to(mouse_pos)

        space.step(delta_ms)

        space.draw_all()

    display.blit(space, (0, 0))
    pygame.display.update()

    # Cap the frame rate to FPS frames per second. Frames can take longer
    # if the frame takes a long time to compute.
    # `delta_ms` is the number of milliseconds since the last frame was
    # rendered, allowing us to scale each step by time elapsed.
    delta_ms = clock.tick(FPS)
pygame.quit()
