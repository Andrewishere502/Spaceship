from pygame import Vector2

from ship import (
    ShipChassis,
    ShipModule,
    WeaponSystem,
)
from components import Health


class Spaceship(ShipChassis):
    def __init__(
        self,
        width: int,
        height: int,
        initial_pos: Vector2,
        initial_health: float,
        max_health: float,
        body_module: ShipModule,
        left_wing_module: ShipModule,
        right_wing_module: ShipModule,
        nose_module: ShipModule,
        tail_module: ShipModule,
        weapon_system: WeaponSystem
    ):
        INITIAL_VEL = Vector2(0, 0)
        INITIAL_ANGLE = 0
        INITIAL_AVEL = 0
        MAX_VEL_COMPONENT = 0.13
        MAX_AVEL = 0

        super().__init__(
            width=width,
            height=height,
            initial_pos=initial_pos,
            initial_vel=INITIAL_VEL,
            initial_angle=INITIAL_ANGLE,
            initial_avel=INITIAL_AVEL,
            max_vel_component=MAX_VEL_COMPONENT,
            max_avel=MAX_AVEL,
            body_module=body_module,
            left_wing_module=left_wing_module,
            right_wing_module=right_wing_module,
            nose_module=nose_module,
            tail_module=tail_module,
            weapon_system=weapon_system,
        )

        self.health = Health(
            initial_health,
            max_health,
        )

        self.score = 0
        self.asteriods_shot = 0
        return

    @property
    def is_alive(self) -> bool:
        return self.health.is_alive

