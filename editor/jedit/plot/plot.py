import matplotlib.pyplot as plt
import ipywidgets as w
from IPython.display import clear_output


class Plot:

    output = w.Output()

    def __init__(self, carousel):
        self.carousel = carousel
        self.updated = False

    def is_user_defined(self) -> bool:
        return self.carousel.has_user_function()

    def update(self) -> None:
        clear_output()
        if self.updated:
            plt.close('all') # very important, possible memory exceeding
        self.carousel.get_current().plot()