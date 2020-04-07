import ipywidgets as w

from .tab import Tab
from ...config import config


class AnalysisTab(Tab):

    def __init__(self, board=None):
        function_manager = board.get_object('function_manager')
        menu = board.get_object('main_menu')
        logger = board.get_object('logger')
        logger_mini_tab = w.Tab(children=[logger.get_widget(t='mini')], layout=w.Layout(height='100%'))
        logger_mini_tab.set_title(0, 'Posledná zmena')
        super().__init__(name='Analýza',
                         main_window=[function_manager.get_plot_widget()],
                         sidebar=[menu.get_widget()],
                         footer=[logger_mini_tab] if config['editor_settings']['footer_log'] == 'yes' else []
                         )

    def get_widget(self) -> w.GridspecLayout:
        grid = w.GridspecLayout(self.board_grid_rows, self.board_grid_cols, height=self.height)
        grid[:self.main_window_rows, :self.main_window_cols] = w.VBox(children=self.main_window)
        grid[:self.main_window_rows, self.main_window_cols:] = w.VBox(children=self.sidebar)
        grid[self.main_window_rows:, :self.board_grid_cols] = w.VBox(children=self.footer)
        return grid


class LogTab(Tab):

    def __init__(self, board=None):
        logger = board.get_object('logger')
        super().__init__(name='Výstupy', main_window=[logger.get_widget(t='main')])

    def get_widget(self) -> w.GridspecLayout:
        grid = w.GridspecLayout(self.board_grid_rows, self.board_grid_cols, height=self.height)
        grid[:self.board_grid_rows, :self.board_grid_cols] = w.VBox(children=self.main_window)
        return grid


class WarningTab(Tab):

    def __init__(self, board=None):
        logger = board.get_object('logger')
        super().__init__(name='Upozornenia', main_window=[logger.get_widget(t='warnings')])

    def get_widget(self) -> w.GridspecLayout:
        grid = w.GridspecLayout(self.board_grid_rows, self.board_grid_cols, height=self.height)
        grid[:self.board_grid_rows, :self.board_grid_cols] = w.VBox(children=self.main_window)
        return grid
