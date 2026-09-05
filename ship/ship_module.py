from pathlib import Path

from pygame import Vector2

from components import Artist


class ShipModule:
    def __init__(
        self,
        image_path: Path,
        pos: Vector2,
        is_mirror_x: bool = False,
        is_mirror_y: bool = False,
    ) -> None:
        """

        :param is_mirror_x: `True` to mirror the image along the x-axis,
            `False` not to.
        :type is_mirror_x: bool, default `False`
        :param is_mirror_y: `True` to mirror the image along the y-axis,
            `False` not to.
        :type is_mirror_y: bool, default `False`
        """
        self.artist = Artist(
            image_path,
            is_mirror_x=is_mirror_x,
            is_mirror_y=is_mirror_y,
        )
        # Position/angle will remain constant.
        self._pos = pos
        return

    @property
    def pos(self) -> Vector2:
        return self._pos
