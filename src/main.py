import pygame
import pygame_gui
import sys
import os
from game_class import *


def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)


class PlayUI:
    def __init__(self, width, height):
        self.manager = pygame_gui.UIManager((width, height))
        self.main_menu_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, 700), (100, 50)),
            text="Main menu",
            manager=self.manager,
        )
        self.save_game_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, 750), (100, 50)),
            text="Save game",
            manager=self.manager,
        )
        self.save_game_button.disable()
        self.start_game_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((200, 750), (150, 50)),
            text="Start game",
            manager=self.manager,
        )
        self.open_cards_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((350, 750), (150, 50)),
            text="Open cards",
            manager=self.manager,
        )
        self.open_cards_button.disable()
        self.more_cards_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((500, 750), (150, 50)),
            text="More cards",
            manager=self.manager,
        )
        self.more_cards_button.disable()
        self.bet_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((650, 750), (150, 50)),
            text="Bet",
            manager=self.manager,
        )
        self.bet_button.disable()
        self.add_bet_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((800, 750), (150, 50)),
            text="Add bet",
            manager=self.manager,
        )
        self.add_bet_button.disable()

    game = Game("player_name")

    def __str__(self):
        return "ui"


class GameVisual(object):
    def __init__(self):
        self.__SCREEN_WIDTH = 1200
        self.__SCRENN_HEIGHT = 800
        self.__CAPTION = "BlackJack"
        path = resource_path(os.path.join("img/icons", "icon.png"))
        self.__icon = pygame.image.load(path)

        self.__TABLE_COLOR = [0, 186, 143]  # switched by font image maybe
        pygame.init()

        pygame.display.set_caption(self.__CAPTION)
        self.window_surface = pygame.display.set_mode(
            (self.__SCREEN_WIDTH, self.__SCRENN_HEIGHT)
        )
        pygame.display.set_icon(self.__icon)
        self.background = pygame.Surface((self.__SCREEN_WIDTH, self.__SCRENN_HEIGHT))
        self.background.fill(pygame.Color(self.__TABLE_COLOR))
        self.clock = pygame.time.Clock()

    def play_game(self):
        ui = PlayUI(self.__SCREEN_WIDTH, self.__SCRENN_HEIGHT)
        run = True
        while run:
            time_delta = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                match event.type:
                    case pygame_gui.UI_BUTTON_PRESSED:
                        match event.ui_element:
                            case ui.main_menu_button:
                                run = False
                            case ui.start_game_button:
                                ui.start_game_button.disable()
                                ui.add_bet_button.enable()
                                ui.bet_button.enable()
                            case ui.add_bet_button:
                                ui.game.bid_more()
                            case ui.bet_button:
                                try:
                                    ui.game.bet()
                                    ui.add_bet_button.disable()
                                    ui.bet_button.disable()
                                    ui.open_cards_button.enable()
                                    ui.more_cards_button.enable()
                                    ui.game.shuffleDeck()
                                    ui.game.moreCards()
                                    ui.game.moreCards()
                                    print(ui.game.__str__())
                                except EmptyBet as e:
                                    print(f"{e} {e.message}")
                                except BetMoreThanInWallet as e:
                                    print(f"{e} {e.message}")
                                except Exception as e:
                                    print(e)
                            case ui.more_cards_button:
                                ui.game.moreCards()
                                print(list_to_string(ui.game.hand))
                            case ui.open_cards_button:
                                ui.game.result()
                                ui.start_game_button.enable()
                                ui.more_cards_button.disable()
                                ui.open_cards_button.disable()
                                print(ui.game.__str__())
                                ui.game.nextGame()

                ui.manager.process_events(event)

            ui.manager.update(time_delta)
            self.window_surface.blit(self.background, (0, 0))
            ui.manager.draw_ui(self.window_surface)

            pygame.display.update()

    def main_menu(self):
        manager = pygame_gui.UIManager((self.__SCREEN_WIDTH, self.__SCRENN_HEIGHT))

        new_game_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((400, 250), (400, 50)),
            text="New game",
            manager=manager,
        )

        load_game_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((400, 320), (400, 50)),
            text="Load game",
            manager=manager,
        )

        table_of_results_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((400, 390), (400, 50)),
            text="Table of results",
            manager=manager,
        )

        quit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((400, 460), (400, 50)),
            text="Quit",
            manager=manager,
        )

        run = True
        while run:
            time_delta = self.clock.tick(60) / 1000
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
                            if table_of_results_button.is_enabled:
                                table_of_results_button.disable()  # just for test disabling buttons
                            else:
                                table_of_results_button.enable()

                manager.process_events(event)

            manager.update(time_delta)
            self.window_surface.blit(self.background, (0, 0))
            manager.draw_ui(self.window_surface)

            pygame.display.update()
        # del manager
        pygame.quit()
        sys.exit()


new_game = GameVisual()
new_game.main_menu()
