import pygame
import pygame_gui
import sys
import os


class spinBox:
    def __init__(self, position):  # TO DO: ADD SIZES
        self.rect = pygame.Rect(position, (85, 60))
        self.image = pygame.Surface(self.rect.size)

        self.buttonRects = [pygame.Rect(50, 5, 30, 20), pygame.Rect(50, 35, 30, 20)]

        self.state = 0
        self.step = 1

        self.status = 0
