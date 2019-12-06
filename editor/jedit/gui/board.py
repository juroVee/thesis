# external modules
import ipywidgets as w

# project-level modules
from ..plot import Plot, FunctionManager

# package-level modules
from .tab import Tab
from .observer import Observer
from .logger import Logger
from .sidebar_elements import (color_picker,
                               dropdown_grid,
                               dropdown_functions,
                               dropdown_functions_not_defined,
                               dropdown_derivative1, dropdown_derivative2, dropdown_derivative3, dropdown_refinement)


class Board:

    def __init__(self, user_data: dict):
        self._init_plot(user_data)
        self._init_logger()
        self._init_tabs()
        self._init_observer()

    def _init_plot(self, user_data: dict):
        self.plot = Plot(FunctionManager(user_data))

    def _init_logger(self):
        self.logger = Logger()

    def _init_tabs(self):
        tab1 = Tab(name='Analysis',
                   main_window=[self.plot.output],
                   sidebar=[(0, dropdown_functions if self.plot.is_user_defined() else dropdown_functions_not_defined),
                            (1, dropdown_grid),
                            (2, color_picker),
                            (4, dropdown_derivative1),
                            (5, dropdown_derivative2),
                            (6, dropdown_derivative3),
                            (8, dropdown_refinement)
                            ]
                   )
        tab2 = Tab(name='Settings')
        tab3 = Tab(name='Log', main_window=[self.logger.output])
        tab4 = Tab(name='Info')
        self.tab_parent = w.Tab(children=[t.get_grid_space() for t in (tab1, tab2, tab3, tab4)])
        for i, tab in enumerate((tab1, tab2, tab3, tab4)):
            self.tab_parent.set_title(i, tab.name)

    def _init_observer(self):
        self.observer = Observer(self)
        self.observer.start()

    def get_plot(self):
        return self.plot

    def get_logger(self):
        return self.logger

    def get_widget(self) -> w.VBox:
        return w.VBox(children=[self.tab_parent])