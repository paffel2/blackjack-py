import pygame
import pygame_gui
import sys
import os
from game_class import *
from surfaces import *


TABLE_COLOR = [0, 186, 143]
SCREEN_WIDTH = 1200
SCRENN_HEIGHT = 800
background = pygame.Surface((SCREEN_WIDTH, SCRENN_HEIGHT))
background.fill(pygame.Color(TABLE_COLOR))
zero_position = (0, 0)
clock = pygame.time.Clock()


def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)


class SheetScene:
    def __init__(self):
        self.scene = pygame.Surface((SCREEN_WIDTH, SCRENN_HEIGHT))
        self.scene.fill(pygame.Color(TABLE_COLOR))
        self.manager = pygame_gui.UIManager((SCREEN_WIDTH, SCRENN_HEIGHT))
        self.main_menu_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((350, 700), (500, 50)),
            text="Main menu",
            manager=self.manager,
        )

        font_of_message = font.Font(None, 30)
        rows = []
        with open("./saves/results.csv", "r", newline="") as read_file:
            fieldnames = ["date", "bet", "result"]
            results_reader = csv.DictReader(read_file, fieldnames)
            for row in results_reader:
                rows.append(row)
        header_date_cell = pygame.Surface((333, 40))
        header_bet_cell = pygame.Surface((333, 40))
        header_result_cell = pygame.Surface((333, 40))
        header_date_cell.fill(pygame.Color(TABLE_COLOR))
        header_result_cell.fill(pygame.Color(TABLE_COLOR))
        header_bet_cell.fill(pygame.Color(TABLE_COLOR))
        pygame.draw.rect(header_date_cell, (0, 0, 0), Rect(0, 0, 333, 40), 1)
        pygame.draw.rect(header_bet_cell, (0, 0, 0), Rect(0, 0, 333, 40), 1)
        pygame.draw.rect(header_result_cell, (0, 0, 0), Rect(0, 0, 333, 40), 1)
        header_date_render_text = font_of_message.render("Date", 1, (0, 0, 0))
        header_bet_render_text = font_of_message.render("Bet", 1, (0, 0, 0))
        header_result_render_text = font_of_message.render("Result", 1, (0, 0, 0))
        header_date_cell.blit(header_date_render_text, (10, 10))
        header_bet_cell.blit(header_bet_render_text, (10, 10))
        header_result_cell.blit(header_result_render_text, (10, 10))
        header_row = RowSurface(
            (999, 40),
            332,
            [header_date_cell, header_bet_cell, header_result_cell],
            TABLE_COLOR,
        )
        list_of_rows = [header_row]
        for row in rows:
            date_cell = pygame.Surface((333, 40))
            bet_cell = pygame.Surface((333, 40))
            result_cell = pygame.Surface((333, 40))
            date_cell.fill(pygame.Color(TABLE_COLOR))
            result_cell.fill(pygame.Color(TABLE_COLOR))
            bet_cell.fill(pygame.Color(TABLE_COLOR))
            pygame.draw.rect(date_cell, (0, 0, 0), Rect(0, 0, 333, 40), 1)
            pygame.draw.rect(result_cell, (0, 0, 0), Rect(0, 0, 333, 40), 1)
            pygame.draw.rect(bet_cell, (0, 0, 0), Rect(0, 0, 333, 40), 1)
            date_render_text = font_of_message.render(row["date"], 1, (0, 0, 0))
            bet_render_text = font_of_message.render(row["bet"], 1, (0, 0, 0))
            result_render_text = font_of_message.render(row["result"], 1, (0, 0, 0))
            date_cell.blit(date_render_text, (10, 10))
            bet_cell.blit(bet_render_text, (10, 10))
            result_cell.blit(result_render_text, (10, 10))

            row = RowSurface(
                (999, 40), 332, [date_cell, bet_cell, result_cell], TABLE_COLOR
            )
            list_of_rows.append(row)

        sheet = SheetSurface((999, 440), 39, list_of_rows, TABLE_COLOR)

        self.scene.blit(sheet, (100, 200))

    def update_scene(self):
        time_delta = clock.tick(60) / 1000
        self.manager.update(time_delta)
        self.manager.draw_ui(self.scene)


class PlayUI:
    def __init__(self, loaded_game=Game()):
        self.scene = pygame.Surface((SCREEN_WIDTH, SCRENN_HEIGHT))
        self.scene.fill(pygame.Color(TABLE_COLOR))

        self.manager = pygame_gui.UIManager((SCREEN_WIDTH, SCRENN_HEIGHT))
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
        self.more_cards_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((500, 750), (150, 50)),
            text="More cards",
            manager=self.manager,
        )
        self.bet_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((650, 750), (150, 50)),
            text="Bet",
            manager=self.manager,
        )
        self.add_bet_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((800, 750), (150, 50)),
            text="Add bet",
            manager=self.manager,
        )

        self.game = loaded_game
        self.font_of_message = pygame.font.Font(None, 36)
        self.wallet_value_text = self.font_of_message.render(
            f"wallet: {self.game.wallet}", 1, (0, 0, 0)
        )
        self.bank_value_text = self.font_of_message.render(
            f"bank: {self.game.bank}", 1, (0, 0, 0)
        )
        self.bid_value_text = self.font_of_message.render(
            f"bid: {self.game.bid}", 1, (0, 0, 0)
        )

        match self.game.game_status:
            case "GAME_STARTED":  # возможно статусы нужно засунуть в класс
                self.start_game_button.disable()
                self.more_cards_button.disable()
                self.open_cards_button.disable()
                self.bet_button.enable()
                self.add_bet_button.enable()

            case "GAME_IN_PROGRESS":
                self.start_game_button.disable()
                self.more_cards_button.enable()
                self.open_cards_button.enable()
                self.bet_button.disable()
                self.add_bet_button.disable()

            case _:
                self.start_game_button.enable()
                self.more_cards_button.disable()
                self.open_cards_button.disable()
                self.bet_button.disable()
                self.add_bet_button.disable()

        self.hand_border = pygame.Surface((938, 170))
        self.hand_border.fill(pygame.Color(TABLE_COLOR))
        pygame.draw.rect(self.hand_border, (0, 0, 0), pygame.Rect(0, 0, 938, 170), 2)
        self.hand_surface = HandSurface((928, 160), TABLE_COLOR)
        self.hand_surface.fill(pygame.Color((TABLE_COLOR)))
        self.hand_border.blit(self.hand_surface, (5, 5))
        self.cards_surfaces = []
        self.clock = pygame.time.Clock()
        self.add_list_of_surfaces()

    def update_money(self):
        self.wallet_value_text = self.font_of_message.render(
            f"wallet: {self.game.wallet}", 1, (0, 0, 0)
        )
        self.bank_value_text = self.font_of_message.render(
            f"bank: {self.game.bank}", 1, (0, 0, 0)
        )
        self.bid_value_text = self.font_of_message.render(
            f"bid: {self.game.bid}", 1, (0, 0, 0)
        )

    def add_and_draw_card_surface(self, card):
        card_image = read_card(card)
        card_image = pygame.transform.scale(card_image, (116, 160))
        card_surface = pygame.Surface((116, 160))
        card_surface.fill(pygame.Color(TABLE_COLOR))
        card_surface.blit(card_image, zero_position)
        self.hand_surface.blit_next(card_surface)
        self.hand_border.blit(self.hand_surface, (5, 5))
        self.cards_surfaces.append(card_surface)

    def add_list_of_surfaces(self):
        for card in self.game.hand:
            self.add_and_draw_card_surface(card)

    def add_last_card(self):
        card = self.game.hand[-1]
        self.add_and_draw_card_surface(card)

    def clean_table(self):
        self.hand_surface.clean_hand()
        self.cards_surfaces = []
        self.hand_border.blit(self.hand_surface, (5, 5))

    def __str__(self):
        return "ui"

    def update_scene(self):
        time_delta = clock.tick(60) / 1000
        self.manager.update(time_delta)
        self.scene.blit(background, zero_position)
        self.scene.blit(self.bank_value_text, (10, 10))
        self.scene.blit(self.wallet_value_text, (200, 10))
        self.scene.blit(self.bid_value_text, (400, 10))
        self.scene.blit(self.hand_border, (90, 500))
        self.manager.draw_ui(self.scene)


class GameVisual(object):
    def __init__(self):
        self.__CAPTION = "BlackJack"
        icon_path = resource_path(os.path.join("./img/icons", "icon.png"))
        self.__icon = pygame.image.load(icon_path)
        pygame.init()

        pygame.display.set_caption(self.__CAPTION)
        self.window_surface = pygame.display.set_mode((SCREEN_WIDTH, SCRENN_HEIGHT))
        pygame.display.set_icon(self.__icon)
        self.clock = pygame.time.Clock()

    def play_game(self, loaded_game=Game()):
        ui = PlayUI(loaded_game)
        run = True
        while run:
            for event in pygame.event.get():
                match event.type:
                    case 9:
                        ui.game.save_game()
                        pygame.quit()
                    case pygame_gui.UI_BUTTON_PRESSED:
                        match event.ui_element:
                            case ui.main_menu_button:
                                run = False
                            case ui.start_game_button:
                                ui.clean_table()
                                ui.start_game_button.disable()
                                ui.add_bet_button.enable()
                                ui.bet_button.enable()
                                ui.update_money()
                                ui.game.game_status = STATUS_STARTED  # перенести в класс Game, там все отрефакторить
                                ui.game.save_game()  # ВОЗМОЖНО ТОЖЕ СТОИТ перенести вызов внутри функций класса
                            case ui.add_bet_button:
                                ui.game.bid_more()
                                ui.update_money()
                                ui.game.save_game()
                            case ui.bet_button:
                                try:
                                    ui.game.bet()
                                    ui.add_bet_button.disable()
                                    ui.bet_button.disable()
                                    ui.open_cards_button.enable()
                                    ui.more_cards_button.enable()
                                    ui.game.moreCards()
                                    ui.game.moreCards()
                                    ui.update_money()
                                    ui.add_list_of_surfaces()
                                    ui.game.game_status = STATUS_IN_PROGRESS  # перенести в класс Game, там все отрефакторить
                                    ui.game.save_game()
                                    print(ui.game.__str__())
                                except EmptyBet as e:
                                    print(f"{e} {e.message}")
                                except BetMoreThanInWallet as e:
                                    print(f"{e} {e.message}")
                                except Exception as e:
                                    print(e)
                            case ui.more_cards_button:
                                try:
                                    ui.game.moreCards()
                                    ui.add_last_card()
                                    ui.game.save_game()
                                    # print(list_to_string(ui.game.hand))
                                except ToMuchCards as e:
                                    print(e.message)
                                except Exception as e:
                                    print(e)
                            case ui.open_cards_button:
                                ui.game.result()
                                ui.start_game_button.enable()
                                ui.more_cards_button.disable()
                                ui.open_cards_button.disable()
                                ui.update_money()
                                # print(ui.game.__str__())
                                ui.game.nextGame()
                                ui.game.save_game()
                            case ui.save_game_button:
                                ui.game.save_game()

                ui.manager.process_events(event)

            ui.update_scene()
            self.window_surface.blit(ui.scene, zero_position)
            pygame.display.update()

    def table_of_results(self):
        sheet_scene = SheetScene()
        run = True
        while run:
            for event in pygame.event.get():
                match event.type:
                    case pygame_gui.UI_BUTTON_PRESSED:
                        match event.ui_element:
                            case sheet_scene.main_menu_button:
                                run = False
                sheet_scene.manager.process_events(event)
            sheet_scene.update_scene()
            self.window_surface.blit(sheet_scene.scene, zero_position)
            pygame.display.update()

    def main_menu(self):
        manager = pygame_gui.UIManager((SCREEN_WIDTH, SCRENN_HEIGHT))

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
            time_delta = clock.tick(60) / 1000
            manager.update(time_delta)
            self.window_surface.blit(background, zero_position)
            manager.draw_ui(self.window_surface)

            pygame.display.update()

        pygame.quit()
        sys.exit()


new_game = GameVisual()
new_game.main_menu()
