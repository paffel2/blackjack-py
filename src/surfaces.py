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


######################################### TABLE SURFACE #############################
class RowSurface(Surface):
    def __init__(self, size, step, list_of_cells):
        Surface.__init__(self, size)
        self.background_color = [0, 186, 143]
        self.list_of_cells = list_of_cells
        self.step = step
        postion = 0
        self.fill(self.background_color)
        for cell in self.list_of_cells:
            self.blit(cell, (postion, 0))
            postion += step


class SheetSurface(Surface):
    def __init__(self, size, step, list_of_rows):
        Surface.__init__(self, size)
        self.background_color = [0, 186, 143]
        self.list_of_rows = list_of_rows
        self.step = step
        postion = 0
        self.fill(self.background_color)
        for row in self.list_of_rows:
            self.blit(row, (0, postion))
            postion += step
