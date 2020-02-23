# external modules
import ipywidgets as w

# project-level modules
from ..plot import Manager

# package-level modules
from .tabs import AnalysisTab, LogTab, WarningTab
from .observer import Observer
from .elements import GUIElementManager


class Board:

    def __init__(self, user_params, logger):
        if 'config' in user_params:
            self.user_config = user_params['config']
        self.logger = logger
        self._init_manager(user_params)
        self._init_gui_elements_manager()
        self._init_tabs()
        self._init_observer()

    def _init_manager(self, user_params: dict) -> None:
        self.manager = Manager(user_params)

    def _init_gui_elements_manager(self) -> None:
        self.gui_manager = GUIElementManager(self.manager)

    def _init_tabs(self):
        tabs = [AnalysisTab(board=self),
                LogTab(board=self),
                WarningTab(board=self)]
        self.tab_parent = w.Tab(children=[tab.get_widget() for tab in tabs])
        for i, tab in enumerate(tabs):
            self.tab_parent.set_title(i, tab.name)

    def _init_observer(self):
        self.observer = Observer(self)
        self.observer.start()

    def get_manager_object(self):
        return self.manager

    def get_logger_object(self):
        return self.logger

    def get_gui_manager_object(self):
        return self.gui_manager

    def get_observer_object(self):
        return self.observer

    def get_widget(self) -> w.VBox:
        return w.VBox(children=[self.tab_parent])