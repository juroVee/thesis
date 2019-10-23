import ipywidgets as widgets
from ipywidgets import Layout, VBox, HBox, Button
from IPython.display import display, Markdown, clear_output
import time


def create_button(description, button_style):
    return Button(description=description,
                  button_style=button_style,
                  layout=Layout(height='auto', width='auto'))

def get_log_output(text):
    print(text)

# left bottom output widget
visible_log = widgets.Output()


# reset button click function
def reset_button_clicked():
      with visible_log:
          clear_output()
          get_log_output('Editor has been successfully reset')
          time.sleep(3)
          clear_output()

# reset button and it's click function init
button_reset = create_button(description='Reset Editor', button_style='')
button_reset.on_click(reset_button_clicked)