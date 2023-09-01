import pygame

TABLE_COLOR: pygame.Color = [0, 186, 143]
SCREEN_WIDTH: int = 1200
SCREEN_HEIGHT: int = 800
BACKGROUND = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
BACKGROUND.fill(pygame.Color(TABLE_COLOR))
ZERO_POSITION = (0, 0)
CLOCK = pygame.time.Clock()
TIME_DELTA: float = CLOCK.tick(60) / 1000
BLACK_COLOR: pygame.Color = (0, 0, 0)
ERROR_COLOR: pygame.Color = (255, 0, 0)
