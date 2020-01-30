# external modules
import matplotlib.pyplot as plt
import ipywidgets as w
from IPython.display import clear_output


class Plot:

    output = w.Output()

    def __init__(self, manager):
        self.function_manager = manager
        self.updated = False

    def is_user_defined(self) -> bool:
        return self.function_manager.has_user_function()

    def update(self) -> None:
        with self.output:
            clear_output()
            if self.updated:
                plt.close('all') # very important, possible memory exceeding
            self.function_manager.get_current().plot()

    def get_widget(self):
        return self.output