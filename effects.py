import pygame

from settings_reader import get_path


class Effect:
    def __init__(self, pos, frames, frame_durration, frame_folder, scale=1, loop=False):
        self.pos = list(pos)

        PATH = get_path() + frame_folder
        # frames should all be the same size!
        self.frames = tuple(map(lambda file_name: PATH + file_name, frames))

        self.current_frame = 0
        self.end_frame = len(frames)

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
        frame = self.frames[self.current_frame]
        image = pygame.image.load(frame)
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
        frame_folder = "Explosion/"
        frames = ("1.png", "2.png", "3.png", "4.png", "5.png", "6.png")
        frame_durration = 5
        super().__init__(pos, frames, frame_durration, frame_folder, scale=scale)
        return


class Danger(Effect):
    def __init__(self, pos):
        frame_folder = "Danger/"
        frames = ("danger-on.png", "danger-off.png")
        frame_durration = 15
        super().__init__(pos, frames, frame_durration, frame_folder, loop=True)
        return
