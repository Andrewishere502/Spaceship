import random
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
from ship import (
    BaseShipModule,
    WeaponSystem,
)
from weapons import (
    PhaseBlaster,
    # PlasmaLauncher,
    # IonFlak,
    # AlloyCannon,
    # IonRing,
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
    Return the keyboard controls mapping.
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


def get_mouse_mapping(
    space: Space,
) -> dict[int, Callable]:
    """
    Return the mouse controls mapping.
    """
    INPUT_MAPPING = {
        pygame.BUTTON_LEFT: space.spaceship_shoot,  # Mouse button left
    }
    return INPUT_MAPPING


def make_spaceship(
    initial_pos: Vector2,
) -> Spaceship:
    """
    Return a new spaceship instance.
    """
    SPACESHIP_SPRITE_DIR = Path('Sprites/spaceships/small/')
    WEAPON_SYSTEM_POS = Vector2(0, 0)
    HEALTH = 10

    weapon_system = WeaponSystem(
        # Position relative to the chassis.
        WEAPON_SYSTEM_POS,
        # List of weapons the system contains.
        [
            PhaseBlaster(),
            # PlasmaLauncher(),
            # IonFlak(),
            # AlloyCannon(),
            # IonRing(),
        ],
    )

    spaceship = Spaceship(
        initial_health=HEALTH,
        max_health=HEALTH,
        initial_pos=initial_pos,
        weapon_system=weapon_system,
    )
    return spaceship


# Maximum frames per second.
FPS = 90

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

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

# Setup the spaceship keyboard and mouse input controllers.
keyboard_controller = InputController()
mouse_controller = InputController()
keyboard_controller.set_map(
    get_keyboard_mapping(
        space,
        spaceship,
    )
)
mouse_controller.set_map(
    get_mouse_mapping(
        space,
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
                keyboard_controller.set_map(
                    get_keyboard_mapping(
                        space,
                        spaceship,
                    )
                )
                mouse_controller.set_map(
                    get_mouse_mapping(
                        space,
                    )
                )
            elif event.key == pygame.K_e:
                spaceship.weapon_system.next_weapon()
            elif event.key == pygame.K_q:
                spaceship.weapon_system.prev_weapon()
            elif event.key == pygame.K_p:
                pause = not pause
            else:
                keyboard_controller.send(event.key)

    if spaceship.is_alive and not pause:
        # For each mapped input on the keyboard, send it to the
        # controller to activate the corresponding action if that key
        # is pressed.
        keys_pressed = pygame.key.get_pressed()
        for keyboard_button_id in set(keyboard_controller._input_map.keys()):
            if keys_pressed[keyboard_button_id]:
                keyboard_controller.send(keyboard_button_id)
        # For each mapped input on the mouse, send it to the controller
        # to activate the corresponding action if that button is pressed.
        mouse_pressed = pygame.mouse.get_pressed()
        for mouse_button_id in set(mouse_controller._input_map.keys()):
            # The index of the mouse button's state is its ID number
            # minus one.
            if mouse_pressed[mouse_button_id - 1]:
                mouse_controller.send(mouse_button_id)

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
