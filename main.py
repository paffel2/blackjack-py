import pygame
import pygame_gui
import sys
import os


def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)

class GameVisual(object):
    def __init__(self):
        self.__SCREEN_WIDTH = 1200
        self.__SCRENN_HEIGHT = 800
        self.__CAPTION = "BlackJack"
        path = resource_path(os.path.join('img/icons', 'icon.png'))
        self.__icon = pygame.image.load(path)
        
        self.__TABLE_COLOR = [0,186,143] #switched by font image maybe
        pygame.init()

        pygame.display.set_caption(self.__CAPTION)
        self.window_surface = pygame.display.set_mode((self.__SCREEN_WIDTH, self.__SCRENN_HEIGHT))
        pygame.display.set_icon(self.__icon)
        self.background = pygame.Surface((self.__SCREEN_WIDTH, self.__SCRENN_HEIGHT))
        self.background.fill(pygame.Color(self.__TABLE_COLOR))
        self.clock = pygame.time.Clock()

    def start_game(self):
        manager = pygame_gui.UIManager((self.__SCREEN_WIDTH, self.__SCRENN_HEIGHT))
        main_menu_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 700), (100, 50)),
                                             text='Main menu',
                                             manager=manager)
        save_game_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 750), (100, 50)),
                                             text='Save game',
                                             manager=manager) 
        
        run = True
        while run:
            time_delta = self.clock.tick(60)/1000.0
            for event in pygame.event.get():
                match event.type:
                    case pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == main_menu_button:
                            run = False
                            self.main_menu()

                manager.process_events(event)

            manager.update(time_delta)
            self.window_surface.blit(self.background, (0, 0))
            manager.draw_ui(self.window_surface)

            pygame.display.update()


    def main_menu(self):
        manager = pygame_gui.UIManager((self.__SCREEN_WIDTH, self.__SCRENN_HEIGHT))

        new_game_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 250), (400, 50)),
                                             text='New game',
                                             manager=manager)
        
        load_game_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 320), (400, 50)),
                                             text='Load game',
                                             manager=manager)

        table_of_results_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 390), (400, 50)),
                                             text='Table of results',
                                             manager=manager)

        quit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 460), (400, 50)),
                                             text='Quit',
                                             manager=manager)

        
        run = True
        while run:
            time_delta = self.clock.tick(60)/1000.0
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
                        if event.ui_element == new_game_button:
                            self.start_game()

                manager.process_events(event)

            manager.update(time_delta)
            self.window_surface.blit(self.background, (0, 0))
            manager.draw_ui(self.window_surface)

            pygame.display.update()
        #del manager
        pygame.quit()
        sys.exit()


new_game = GameVisual()
new_game.main_menu()
