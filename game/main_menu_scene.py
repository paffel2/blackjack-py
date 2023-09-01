import pygame
import pygame_gui
from .constants import *
from .game_class.common import *
from .game_class.game_class import *
import sys
import os
from .game_scene import GameScene
from .sheet_scene import SheetScene


class MainMenuScene:
    def __init__(self):
        self.__CAPTION = "BlackJack"
        icon_path = resource_path(os.path.join("./img/icons", "icon.png"))
        self.__icon = pygame.image.load(icon_path)
        pygame.init()

        pygame.display.set_caption(self.__CAPTION)
        self.window_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_icon(self.__icon)
        self.clock = pygame.time.Clock()

    def play_game(self, loaded_game=Game()):
        game_scene = GameScene(loaded_game)
        while game_scene.play_game():
            self.window_surface.blit(game_scene.scene, ZERO_POSITION)
            pygame.display.update()

    def table_of_results(self):
        sheet_scene = SheetScene()
        while sheet_scene.show_scene():
            self.window_surface.blit(sheet_scene.scene, ZERO_POSITION)
            pygame.display.update()

    def main_menu(self):
        manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
        button_size = (400, 50)

        new_game_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((400, 250), button_size),
            text="New game",
            manager=manager,
        )

        load_game_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((400, 320), button_size),
            text="Load game",
            manager=manager,
        )

        table_of_results_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((400, 390), button_size),
            text="Table of results",
            manager=manager,
        )

        quit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((400, 460), button_size),
            text="Quit",
            manager=manager,
        )

        run = True
        while run:
            for event in pygame.event.get():
                match event.type:
                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_ESCAPE:
                                run = False

                    case pygame.QUIT:
                        run = False
                    case pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == quit_button:
                            run = False
                        elif event.ui_element == new_game_button:
                            self.play_game()
                        elif event.ui_element == load_game_button:
                            loaded_game = load_game()
                            self.play_game(loaded_game)
                        elif event.ui_element == table_of_results_button:
                            self.table_of_results()
                manager.process_events(event)
            manager.update(TIME_DELTA)
            self.window_surface.blit(BACKGROUND, ZERO_POSITION)
            manager.draw_ui(self.window_surface)

            pygame.display.update()

        pygame.quit()
        sys.exit()
