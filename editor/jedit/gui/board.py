# external modules
import ipywidgets as w

# project-level modules
from ..plot import Plot, Manager

# package-level modules
from .tabs import AnalysisTab, SettingsTab, LogTab, InfoTab
from .observer import Observer
from .elements import GUIElementManager


class Board:

    def __init__(self, user_params, logger):
        self.logger = logger
        self._init_plot(user_params)
        self._init_gui_elements_manager()
        self._init_tabs()
        self._init_observer()

    def _init_plot(self, user_data: dict):
        self.plot = Plot(Manager(user_data))

    def _init_gui_elements_manager(self):
        self.gui_manager = GUIElementManager(self.plot.is_user_defined())

    def _init_tabs(self):
        tabs = [AnalysisTab(board=self),
                SettingsTab(board=self),
                LogTab(board=self),
                InfoTab(board=self)]
        self.tab_parent = w.Tab(children=[tab.get_widget() for tab in tabs])
        for i, tab in enumerate(tabs):
            self.tab_parent.set_title(i, tab.name)

    def _init_observer(self):
        self.observer = Observer(self)
        self.observer.start()

    def get_plot_object(self):
        return self.plot

    def get_logger_object(self):
        return self.logger

    def get_gui_manager_object(self):
        return self.gui_manager

    def get_widget(self) -> w.VBox:
        return w.VBox(children=[self.tab_parent])