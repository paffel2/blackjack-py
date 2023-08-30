import pygame
import pygame_gui
import constants
import surfaces
import game_class


class GameScene:
    def __init__(self, loaded_game=game_class.Game()):
        self.scene = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.scene.fill(pygame.Color(constants.TABLE_COLOR))

        self.manager = pygame_gui.UIManager(
            (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
        )
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
            f"wallet: {self.game.wallet}", 1, constants.BLACK_COLOR
        )
        self.bank_value_text = self.font_of_message.render(
            f"bank: {self.game.bank}", 1, constants.BLACK_COLOR
        )
        self.bid_value_text = self.font_of_message.render(
            f"bid: {self.game.bid}", 1, constants.BLACK_COLOR
        )

        match self.game.game_status:
            case game_class.GameStatus.STATUS_STARTED:
                self.start_game_button.disable()
                self.more_cards_button.disable()
                self.open_cards_button.disable()
                self.bet_button.enable()
                self.add_bet_button.enable()

            case game_class.GameStatus.STATUS_IN_PROGRESS:
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
        self.hand_border.fill(pygame.Color(constants.TABLE_COLOR))
        pygame.draw.rect(
            self.hand_border, constants.BLACK_COLOR, pygame.Rect(0, 0, 938, 170), 2
        )
        self.hand_surface = surfaces.HandSurface((928, 160), constants.TABLE_COLOR)
        self.hand_surface.fill(pygame.Color((constants.TABLE_COLOR)))
        self.hand_border.blit(self.hand_surface, (5, 5))
        self.cards_surfaces = []
        self.draw_list_of_surfaces()
        self.message_surface = pygame.Surface((800, 200))
        self.message_surface.fill(pygame.Color(255, 160, 122))  # TABLE_COLOR

    def draw_message(self, text):
        render_text = self.font_of_message.render(text, 1, constants.BLACK_COLOR)
        self.message_surface.blit(render_text, (100, 70))

    def clean_message_surface(self):
        self.message_surface.fill(pygame.Color(255, 160, 122))

    def update_money(self):
        self.wallet_value_text = self.font_of_message.render(
            f"wallet: {self.game.wallet}", 1, constants.BLACK_COLOR
        )
        self.bank_value_text = self.font_of_message.render(
            f"bank: {self.game.bank}", 1, constants.BLACK_COLOR
        )
        self.bid_value_text = self.font_of_message.render(
            f"bid: {self.game.bid}", 1, constants.BLACK_COLOR
        )

    def draw_card_surface(self, card):
        card_image = game_class.read_card(card)
        card_image = pygame.transform.scale(card_image, (116, 160))
        card_surface = pygame.Surface((116, 160))
        card_surface.fill(pygame.Color(constants.TABLE_COLOR))
        card_surface.blit(card_image, constants.ZERO_POSITION)
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
        self.manager.update(constants.TIME_DELTA)
        self.scene.fill(constants.TABLE_COLOR)
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
                        self.game.save_game()
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
                                self.game.game_status = (
                                    game_class.GameStatus.STATUS_STARTED
                                )  # перенести в класс Game, там все отрефакторить
                                self.game.save_game()
                                self.clean_message_surface()
                            case self.add_bet_button:
                                try:
                                    self.game.bid_more()
                                    self.update_money()
                                    self.game.save_game()
                                    self.clean_message_surface()
                                except game_class.BetMoreThanInWallet as e:
                                    self.draw_message(e.message)
                                except game_class.BetMoreThanInBank as e:
                                    self.draw_message(e.message)
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
                                        game_class.GameStatus.STATUS_IN_PROGRESS
                                    )  # возможно нужен метод для класса Game который управляет ходом игры
                                    self.game.save_game()
                                    self.clean_message_surface()
                                except game_class.EmptyBet as e:
                                    self.draw_message(e.message)
                                except game_class.BetMoreThanInWallet as e:
                                    self.draw_message(e.message)
                                except Exception as e:
                                    self.draw_message(str(e))
                            case self.more_cards_button:
                                try:
                                    self.game.moreCards()
                                    self.draw_last_card()
                                    self.game.save_game()
                                    self.clean_message_surface()
                                except game_class.ToMuchCards as e:
                                    self.draw_message(e.message)
                                except Exception as e:
                                    self.draw_message(str(e))
                            case self.open_cards_button:
                                result = self.game.result()
                                self.start_game_button.enable()
                                self.more_cards_button.disable()
                                self.open_cards_button.disable()
                                self.update_money()
                                self.game.nextGame()
                                self.game.save_game()
                                self.draw_message(result)
                            case self.save_game_button:
                                self.game.save_game()

                self.manager.process_events(event)

            self.update_scene()
            return run
