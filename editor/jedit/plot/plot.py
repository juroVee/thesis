import matplotlib.pyplot as plt
import ipywidgets as w
from .carousel import FunctionCarousel


class Plot:

    output = w.Output()

    def __init__(self, fig, ax):
        self.carousel = FunctionCarousel(fig, ax)
        self.updated = False

    def is_user_defined(self) -> bool:
        return self.carousel.has_user_function()

    def update(self) -> None:
        if self.updated:
            plt.close('all') # very important, possible memory exceeding
        self.carousel.get_current().plot()