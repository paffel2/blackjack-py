from pygame import *


class HandSurface(Surface):
    def __init__(self, size):
        Surface.__init__(self, size)
        self.last_position = 0
        self.step = 116
        self.background_color = [0, 186, 143]

    def blit_next(self, surface):
        self.blit(surface, (self.last_position, 0))
        self.last_position += self.step

    def clean_hand(self):
        self.fill(Color(self.background_color))
        self.last_position = 0


# a = Surface()
