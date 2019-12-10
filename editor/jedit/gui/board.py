# external modules
import ipywidgets as w

# project-level modules
from ..plot import Plot, FunctionManager

# package-level modules
from .tab import Tab
from .observer import Observer
from .logger import Logger
from .elements import GUIElementManager


class Board:

    def __init__(self, user_data: dict):
        self._init_plot(user_data)
        self._init_logger()
        self._init_gui_elements_manager()
        self._init_tabs()
        self._init_observer()

    def _init_plot(self, user_data: dict):
        self.plot = Plot(FunctionManager(user_data))

    def _init_logger(self):
        self.logger = Logger()

    def _init_gui_elements_manager(self):
        self.gui_manager = GUIElementManager(self.plot.is_user_defined())

    def _init_tabs(self):
        gui_elements = self.gui_manager.get_elements()
        tab1 = Tab(name='Analysis',
                   main_window=[self.plot.get_widget()],
                   sidebar=[(0, gui_elements['hbox_function']),
                            (1, gui_elements['dropdown_grid']),
                            (3, gui_elements[f'hbox_derivative1']),
                            (4, gui_elements[f'hbox_derivative2']),
                            (5, gui_elements[f'hbox_derivative3']),
                            (7, gui_elements['dropdown_refinement']),
                            (8, gui_elements['hbox_zero_points'])
                            ]
                   )
        tab2 = Tab(name='Settings')
        tab3 = Tab(name='Log', main_window=[self.logger.get_widget()])
        tab4 = Tab(name='Info')
        self.tab_parent = w.Tab(children=[t.get_grid_space() for t in (tab1, tab2, tab3, tab4)])
        for i, tab in enumerate((tab1, tab2, tab3, tab4)):
            self.tab_parent.set_title(i, tab.name)

    def _init_observer(self):
        self.observer = Observer(self)
        self.observer.start()

    def get_plot_object(self):
        return self.plot

    def get_logger_object(self):
        return self.logger

    def get_gui_manager(self):
        return self.gui_manager

    def get_widget(self) -> w.VBox:
        return w.VBox(children=[self.tab_parent])