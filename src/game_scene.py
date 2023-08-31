import pygame
import pygame_gui
from .constants import *
from .surfaces import *
from .game_class import *
from .exceptions import *


class GameScene:
    def __init__(self, loaded_game=Game()):
        self.scene = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.scene.fill(pygame.Color(TABLE_COLOR))

        self.manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
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
            f"wallet: {self.game.wallet}", 1, BLACK_COLOR
        )
        self.bank_value_text = self.font_of_message.render(
            f"bank: {self.game.bank}", 1, BLACK_COLOR
        )
        self.bid_value_text = self.font_of_message.render(
            f"bid: {self.game.bid}", 1, BLACK_COLOR
        )

        match self.game.game_status:
            case GameStatus.STATUS_STARTED:
                self.start_game_button.disable()
                self.more_cards_button.disable()
                self.open_cards_button.disable()
                self.bet_button.enable()
                self.add_bet_button.enable()

            case GameStatus.STATUS_IN_PROGRESS:
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
        pygame.draw.rect(self.hand_border, BLACK_COLOR, pygame.Rect(0, 0, 938, 170), 2)
        self.hand_surface = HandSurface((928, 160), TABLE_COLOR)
        self.hand_surface.fill(pygame.Color((TABLE_COLOR)))
        self.hand_border.blit(self.hand_surface, (5, 5))
        self.cards_surfaces = []
        self.draw_list_of_surfaces()
        self.message_surface = pygame.Surface((800, 200))
        self.message_surface.fill(TABLE_COLOR)

    def clean_message_surface(self):
        self.message_surface.fill(TABLE_COLOR)

    def draw_message(self, text, color=TABLE_COLOR):
        render_text = self.font_of_message.render(text, 1, BLACK_COLOR)
        self.message_surface.fill(color)
        self.message_surface.blit(render_text, (100, 70))

    def update_money(self):
        self.wallet_value_text = self.font_of_message.render(
            f"wallet: {self.game.wallet}", 1, BLACK_COLOR
        )
        self.bank_value_text = self.font_of_message.render(
            f"bank: {self.game.bank}", 1, BLACK_COLOR
        )
        self.bid_value_text = self.font_of_message.render(
            f"bid: {self.game.bid}", 1, BLACK_COLOR
        )

    def draw_card_surface(self, card):
        card_image = read_card(card)
        card_image = pygame.transform.scale(card_image, (116, 160))
        card_surface = pygame.Surface((116, 160))
        card_surface.fill(pygame.Color(TABLE_COLOR))
        card_surface.blit(card_image, ZERO_POSITION)
        self.hand_surface.blit_next(card_surface)
        self.hand_border.blit(self.hand_surface, (5, 5))
        self.cards_surfaces.append(card_surface)

    def draw_list_of_surfaces(self):
        for card in self.game.hand:
            self.draw_card_surface(card)

    def draw_last_card(self):
        card = self.game.hand[-1]
        self.draw_card_surface(card)

    def clean_table(self):
        self.hand_surface.clean_hand()
        self.cards_surfaces = []
        self.hand_border.blit(self.hand_surface, (5, 5))

    def __str__(self):
        return "ui"

    def update_scene(self):
        self.manager.update(TIME_DELTA)
        self.scene.fill(TABLE_COLOR)
        self.scene.blit(self.bank_value_text, (10, 10))
        self.scene.blit(self.wallet_value_text, (200, 10))
        self.scene.blit(self.bid_value_text, (400, 10))
        self.scene.blit(self.hand_border, (131, 500))
        self.scene.blit(self.message_surface, (200, 200))
        self.manager.draw_ui(self.scene)

    def play_game(self):
        run = True
        while run:
            for event in pygame.event.get():
                match event.type:
                    case 9:
                        save_game(self.game)
                        pygame.quit()
                    case pygame_gui.UI_BUTTON_PRESSED:
                        match event.ui_element:
                            case self.main_menu_button:
                                run = False
                            case self.start_game_button:
                                self.clean_table()
                                self.start_game_button.disable()
                                self.add_bet_button.enable()
                                self.bet_button.enable()
                                self.update_money()
                                self.game.game_status = GameStatus.STATUS_STARTED
                                save_game(self.game)
                                self.clean_message_surface()
                            case self.add_bet_button:
                                try:
                                    self.game.bid_more()
                                    self.update_money()
                                    save_game(self.game)
                                    self.clean_message_surface()
                                except BetMoreThanInWallet as e:
                                    self.draw_message(e.message, ERROR_COLOR)
                                except BetMoreThanInBank as e:
                                    self.draw_message(e.message, ERROR_COLOR)
                            case self.bet_button:
                                try:
                                    self.game.bet()
                                    self.add_bet_button.disable()
                                    self.bet_button.disable()
                                    self.open_cards_button.enable()
                                    self.more_cards_button.enable()
                                    self.game.moreCards()
                                    self.game.moreCards()
                                    self.update_money()
                                    self.draw_list_of_surfaces()
                                    self.game.game_status = (
                                        GameStatus.STATUS_IN_PROGRESS
                                    )
                                    save_game(self.game)
                                    self.clean_message_surface()
                                except EmptyBet as e:
                                    self.draw_message(e.message, ERROR_COLOR)
                                except BetMoreThanInWallet as e:
                                    self.draw_message(e.message, ERROR_COLOR)
                                except Exception as e:
                                    self.draw_message(str(e), ERROR_COLOR)
                            case self.more_cards_button:
                                try:
                                    self.game.moreCards()
                                    self.draw_last_card()
                                    save_game(self.game)
                                    self.clean_message_surface()
                                except ToMuchCards as e:
                                    self.draw_message(e.message, ERROR_COLOR)
                                except Exception as e:
                                    self.draw_message(str(e), ERROR_COLOR)
                            case self.open_cards_button:
                                self.game.result()
                                result = recalculate_score(self.game)
                                result_color = (255, 165, 0)
                                self.draw_message(result, result_color)
                                add_result_to_history(self.game)
                                self.start_game_button.enable()
                                self.more_cards_button.disable()
                                self.open_cards_button.disable()
                                self.update_money()
                                self.game.nextGame()
                                save_game(self.game)
                            case self.save_game_button:
                                save_game(self.game)

                self.manager.process_events(event)

            self.update_scene()
            return run
