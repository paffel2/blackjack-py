from pygame import *


class HandSurface(Surface):
    def __init__(self, size, background_color):
        Surface.__init__(self, size)
        self.last_position = 0
        self.step = 116
        self.background_color = background_color

    def blit_next(self, surface):
        self.blit(surface, (self.last_position, 0))
        self.last_position += self.step

    def clean_hand(self):
        self.fill(Color(self.background_color))
        self.last_position = 0


class CellSurface(Surface):
    def __init__(self, size, background_color, font, text):
        Surface.__init__(self, size)
        self.background_color = background_color
        self.fill(self.background_color)
        draw.rect(self, (0, 0, 0), Rect(0, 0, size[0], size[1]), 1)
        self.render_text = font.render(text, 1, (0, 0, 0))
        self.blit(self.render_text, (10, 10))


class RowSurface(Surface):
    def __init__(self, size, step, list_of_cells, background_color):
        Surface.__init__(self, size)
        self.background_color = background_color
        self.list_of_cells = list_of_cells
        self.step = step
        postion = 0
        self.fill(self.background_color)
        for cell in self.list_of_cells:
            self.blit(cell, (postion, 0))
            postion += step


class SheetSurface(Surface):
    def __init__(self, size, step, list_of_rows, background_color):
        Surface.__init__(self, size)
        self.background_color = background_color
        self.list_of_rows = list_of_rows
        self.step = step
        postion = 0
        self.fill(self.background_color)
        for row in self.list_of_rows:
            self.blit(row, (0, postion))
            postion += step
