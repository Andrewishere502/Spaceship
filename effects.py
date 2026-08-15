from pathlib import Path

import pygame


class Effect:
    def __init__(self, pos, frame_paths, frame_durration, scale=1, loop=False):
        self.pos = list(pos)

        self.frame_paths = frame_paths

        self.current_frame = 0
        self.end_frame = len(frame_paths)

        self.current_durration = 0
        self.frame_durration = frame_durration

        self.scale = scale

        self.loop = loop
        self.done = False
        return

    def tick(self):
        self.current_durration += 1
        if self.current_durration == self.frame_durration:
            self.next_frame()
        return

    def next_frame(self):
        self.current_frame += 1
        self.current_durration = 1
        if self.current_frame == self.end_frame:
            if self.loop:
                self.current_durration = 0
                self.current_durration = 1
            else:
                self.done = True
        return

    def get_frame(self):
        frame = self.frame_paths[self.current_frame]
        image = pygame.image.load(frame).convert_alpha()
        if self.scale != 1:
            image = pygame.transform.scale(image, (round(image.get_width() * self.scale),
                                                   round(image.get_height() * self.scale)))
        return image

    def set_center(self, center_pos):
        # frames should all be the same size!
        width = self.get_frame().get_width()
        height = self.get_frame().get_height()
        self.pos[0] = center_pos[0] - width // 2
        self.pos[1] = center_pos[1] - height // 2
        return


class Explosion(Effect):
    def __init__(self, pos, scale):
        FRAME_DURRATION = 5

        FRAME_PATHS = [Path('Sprites', 'Explosion', f'{frame_n}.png')
                       for frame_n in range(1, 7)]

        super().__init__(
            pos,
            FRAME_PATHS,
            FRAME_DURRATION,
            scale=scale
        )
        return
