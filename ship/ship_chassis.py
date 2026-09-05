import pygame

from .ship_modules.base_ship_module import BaseShipModule


class ShipChassis:
    def __init__(
        self,
        module_layout: dict[tuple[float, float], BaseShipModule],
    ) -> None:
        """
        Initialize the ship chassis.

        :param module_layout:
        :type module_layout: dict[tuple[float, float], BaseShipModule]
        """
        # Construct the dict storing the current layout for this
        # chassis. I.e. what modules are actually in each available
        # position.
        self._module_layout = module_layout

        # Construct the dict storing what modules types are allowed in
        # each available position.
        self._module_type_layout: dict[tuple[float, float], type[BaseShipModule]] = {}
        for pos, module in self._module_layout.items():
            self._module_type_layout[pos] = type(module)
        return

    def set_module(
        self,
        pos: tuple[float, float],
        new_module: BaseShipModule,
    ) -> BaseShipModule:
        """
        :param pos:
        :type pos: tuple[float, float]
        :param new_module:
        :type new_module: BaseShipModule
        :return:
        :rtype: BaseShipModule
        :raise ValueError: If the given position is not a valid key in
            the `module_type_layout` attribute.
        """
        self._validate_pos(pos)  # Validate the position.

        # If the given module is not of the allowed type, raise an
        # error.
        valid_module_type = self._module_type_layout[pos]
        if not isinstance(new_module, valid_module_type):
            raise ValueError(
                f'Module type {type(new_module)} is not allowed type {valid_module_type}'
            )

        # Replace the old module with the new one, then return the old
        # module.
        old_module = self._module_layout.pop(pos)
        self._module_layout[pos] = new_module
        return old_module

    def get_module(
        self,
        pos: tuple[float, float],
    ) -> BaseShipModule:
        """
        Return the module at the given position.

        :param pos:
        :type pos: tuple[float, float]
        :return:
        :rtype: BaseShipModule
        :raise ValueError: If the given position is not a valid key in
            the `module_type_layout` attribute.
        """
        self._validate_pos(pos)  # Validate the position.
        return self._module_layout[pos]

    def get_image(self, angle: float) -> pygame.surface.Surface:
        """
        Return the spaceship's image, rotated to the direction the
        spaceship is facing. Includes the currently equiped weapon.

        :param angle: Angle to rotate the base image, in degrees.
        :type angle: float
        :return: The rotated image of the ship chassis and its
            components.
        :rtype: pygame.surface.Surface
        """
        image = self.base_image.copy()

        # Rotate the image in the direction the chassis is facing.
        image = pygame.transform.rotate(image, angle)
        return image

    def load_base_image(self) -> None:
        """
        Initialize the base image by combining the images of all ship
        modules onto the same surface.
        """
        # Calculate the necessary width and height of the assembled
        # module images.
        combined_width = 0
        combined_height = 0
        for pos, module in self._module_layout.items():
            module_image = module.artist.get_image(0)
            required_width = pos[0] + module_image.get_width()
            required_height = pos[1] + module_image.get_height()
            if combined_width < required_width:
                combined_width = required_width
            if combined_height < required_height:
                combined_height = required_height

        # Assemble the module images into one single image.
        base_image = pygame.surface.Surface((combined_width, combined_height))
        base_image = base_image.convert_alpha()
        base_image.fill((0, 0, 0, 0))

        # Draw all the modules onto the surface.
        for pos, module in self._module_layout.items():
            module_image = module.artist.get_image(0)
            # Draw the image onto the surface.
            base_image.blit(module_image, pos)

        self._base_image = base_image
        return

    def _validate_pos(self, pos: tuple[float, float]) -> None:
        """
        Raise an error if the given position is not a valid key in the
        `module_type_layout` attribute.

        :param pos: Position to validate.
        :type pos: tuple[float, float]
        :raise ValueError: If the given position is not a valid key in
            the `module_type_layout` attribute.
        """
        if self._module_type_layout.get(pos) is None:
            raise ValueError(f'Invalid module position {pos}')
        return

    @property
    def base_image(self) -> pygame.surface.Surface:
        """
        Return the base image.

        :raise AttributeError: 
        """
        if hasattr(self, '_base_image') is False:
            raise AttributeError(
                'Base image has not been loaded. Call `load_base_image`' \
                ' once before accessing this attribute.'
            )
        else:
            return self._base_image
