import ipywidgets as w
import matplotlib.pyplot as plt
import warnings
from IPython.display import clear_output, display

from .function import Function, DefaultFunction, UserFunction
from .computations import ComputationsManager
from .warn import WarningsManager
from ..settings import settings


class FunctionManager:

    def __init__(self, user_parameters, logger):
        self.output = w.Output(layout=w.Layout(overflow='hidden'))
        plt.ioff()
        self.fig, self.ax = plt.subplots()
        self.fig.set_size_inches(settings['plot_parameters']['width'], settings['plot_parameters']['height'])
        plt.subplots_adjust(left=0.08, bottom=0.08, right=0.92, top=0.92, wspace=0, hspace=0)
        if bool(user_parameters):
            function = UserFunction(user_parameters)
        else:
            parameters = settings['main_function']['default']
            function = DefaultFunction(parameters['name'], parameters)
        self.function = function
        self.updates = 0
        self.warnings = WarningsManager(logger)

    def get_function(self) -> Function:
        return self.function

    def update_plot(self, **kwargs) -> None:
        if len(kwargs) > 0:
            manager = ComputationsManager(function=self.get_function())
            for arg, value in kwargs.items():
                if value:
                    with warnings.catch_warnings(record=True) as warnings_list:
                        warnings.simplefilter("always")
                        getattr(manager, arg)()
                        self.warnings.add(warnings_list)
        self.warnings.print()
        if self.updates > 0:
            plt.close('all')
        function = self.get_function()
        function.plot(self.ax)
        self.updates += 1
        with self.output:
            clear_output(wait=True)
            display(self.ax.figure)
        plt.ion()

    def get_plot_widget(self):
        return self.output
