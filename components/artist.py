from pathlib import Path

import pygame


class Artist:
    def __init__(
        self,
        image_path: Path,
        is_convert_alpha: bool = True,
    ) -> None:

        self.set_base_image(
            image_path,
            is_convert_alpha
        )
        return

    def get_image(self, angle: float) -> pygame.surface.Surface:
        """
        Return the base image, rotated to the given angle.

        :param angle:
        :type angle: 
        :return: The rotated base image.
        :rtype: pygame.surface.Surface
        """
        image = pygame.transform.rotate(
            self._base_image,
            angle,
        )
        return image

    def blit(
        self,
        surf: pygame.surface.Surface,
        rect: pygame.rect.Rect,
    ) -> None:
        """
        Draw the given surface onto a rectangle within this artist's
        base image.

        :param surf: Surface to draw onto this artist's base image.
        :type surf: pygame.surface.Surface
        :param rect: Rectangle defined relative to the base image.
        :type rect: pygame.rect.Rect
        """
        self._base_image.blit(surf, rect)
        return

    def set_base_image(
        self,
        image_path: Path,
        is_convert_alpha: bool = True,
    ) -> None:
        """
        Load the base image for the artist.

        :param image_path: Path to the image to load.
        :type image_path: Path
        :param is_convert_alpha: Whether to enable the alpha channel in
            the loaded image.
        :type is_convert_alpha: bool, default `True`
        """
        base_image = pygame.image.load(image_path)

        # Enable the alpha channels if desired.
        if is_convert_alpha:
            base_image = base_image.convert_alpha()

        self._base_image = base_image
        return
