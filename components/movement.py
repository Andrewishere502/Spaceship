from pygame import Vector2


class Movement:
    """
    Class to manage the position, tangential/rotational velocity of
    some entity.
    """
    def __init__(
        self,
        initial_pos: Vector2,
        initial_vel: Vector2,
        initial_angle: float,
        initial_avel: float,
        max_vel_component: float,
        max_avel: float,
    ) -> None:
        """
        Initialize the `Movement` object.

        :param initial_pos: 
        :type initial_pos: Vector2
        :param initial_vel: Initial tangential velocity of the entity.
        :type initial_vel: Vector2
        :param initial_angle:
        :type initial_angle: Vector2
        :param initial_avel:
        :type initial_avel: Vector2
        :param max_vel_component:
        :type max_vel_component: Vector2
        :param max_avel:
        :type max_avel: Vector2
        """
        self._max_vel_component = max_vel_component
        self._max_avel = max_avel

        self.set_pos(initial_pos)
        self.set_vel(initial_vel)
        self.set_angle(initial_angle)
        self._avel = initial_avel
        return

    def step(self, dt: float) -> None:
        """
        Update the movement component:
            1. Apply the current velocity to the current position, scaled
            by `dt`.
        """
        self._pos += self._vel * dt
        self._angle += (self._avel * dt) % 360
        return

    def apply_acceleration(self, acceleration: Vector2) -> None:
        """
        Apply an acceleration vector to the velocity.

        :param acceleration: Acceleration applied to the velocity.
        :type acceleration: Vector2
        """
        self._vel += acceleration
        self.clip_vel()
        return

    def rotate(self, degrees: float) -> None:
        """
        Rotate the entity by the given number of degrees.

        :param angle_degreees: 
        :type angle_degreees: float
        """
        self._angle += degrees
        return

    def apply_angular_acceleration(self, angular_acceleration: float) -> None:
        """
        Apply angular acceleration to the angular velocity.

        :param angular_acceleration: Angular acceleration applied to
            the angular velocity.
        :type angular_acceleration: float
        """
        self._avel += angular_acceleration

        # Clip the angular velocity to maximum..
        self._avel = (min(abs(self._avel), self._max_avel)
                      * (-1 if self._max_avel < 0 else 1))
        return

    def clip_vel(self) -> None:
        """
        Constrain the magnitude of the x/y components of the velocity
        to a maximum.
        """
        # Constrain the magnitude of the x/y components of the
        # velocity to a maximum.
        self._vel.x = (min(abs(self._vel.x), self._max_vel_component)
                       * (-1 if self._vel.x < 0 else 1))
        self._vel.y = (min(abs(self._vel.y), self._max_vel_component)
                       * (-1 if self._vel.y < 0 else 1))
        return

    ###### Setters ############################

    def set_pos(self, pos: Vector2) -> None:
        """
        Set the entity's position.

        :param pos: New position vector.
        :type pos: Vector2
        """
        self._pos = pos
        return

    def set_vel(self, vel: Vector2) -> None:
        """
        Set the entity's velocity.

        :param vel: New velocity vector.
        :type vel: Vector2
        """
        self._vel = vel
        self.clip_vel()
        return

    def set_angle(self, angle: float) -> None:
        """
        Set the entity's angle.

        :param angle: New angle for the entity.
        :type angle: float
        """
        self._angle = angle
        return

    ####### Getters ############################

    def get_pos(self) -> Vector2:
        """
        Return a copy of the current position as a 2D vector.
        """
        return self._pos.copy()

    def get_vel(self) -> Vector2:
        """
        Return a copy of the current velocity as a 2D vector.
        """
        return self._vel.copy()

    def get_angle(self) -> float:
        """
        Return the current angle of the entity.
        """
        return self._angle

    def get_avel(self) -> float:
        """
        Return the current angular velocity.
        """
        return self._avel
