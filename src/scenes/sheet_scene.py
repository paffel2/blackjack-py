import pygame
import pygame_gui
import constants
import common
import surfaces


class SheetScene:
    def __init__(self):
        self.scene = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.scene.fill(pygame.Color(constants.TABLE_COLOR))
        self.manager = pygame_gui.UIManager(
            (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
        )
        self.main_menu_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((350, 700), (500, 50)),
            text="Main menu",
            manager=self.manager,
        )

        font_of_message = pygame.font.Font(None, 30)

        def create_cell(text):
            return surfaces.CellSurface(
                (333, 40), constants.TABLE_COLOR, font_of_message, text
            )

        rows = []
        common.read_csv_to_list(rows)
        header_date_cell = create_cell("Date")
        header_bet_cell = create_cell("Bet")
        header_result_cell = create_cell("Result")
        header_row = surfaces.RowSurface(
            (999, 40),
            332,
            [header_date_cell, header_bet_cell, header_result_cell],
            constants.TABLE_COLOR,
        )
        list_of_rows = [header_row]
        for row in rows:
            date_cell = create_cell(row["date"])
            bet_cell = create_cell(row["bet"])
            result_cell = create_cell(row["result"])
            row = surfaces.RowSurface(
                (999, 40),
                332,
                [date_cell, bet_cell, result_cell],
                constants.TABLE_COLOR,
            )
            list_of_rows.append(row)

        sheet = surfaces.SheetSurface(
            (999, 440), 39, list_of_rows, constants.TABLE_COLOR
        )

        self.scene.blit(sheet, (100, 200))
        self.manager.draw_ui(self.scene)

    def update_scene(self):
        self.manager.update(constants.TIME_DELTA)
        self.manager.draw_ui(self.scene)

    def show_scene(self):
        run = True
        for event in pygame.event.get():
            match event.type:
                case pygame_gui.UI_BUTTON_PRESSED:
                    match event.ui_element:
                        case self.main_menu_button:
                            run = False
            self.manager.process_events(event)
        self.update_scene()
        return run
