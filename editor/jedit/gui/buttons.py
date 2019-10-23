import time, ipywidgets as w
from .button import Button
from .outputs import print_output, log_output
from IPython.display import clear_output

# ----------- resetting button ----------
reset_button = Button(description='Reset Editor', button_style='').get_widget()

def reset_button_clicked():
    with log_output:
        clear_output()
        #editor.reset()
        print_output('Editor has been successfully reset')
        time.sleep(3)
        clear_output()

@reset_button.on_click
def reset_on_click(b):
    reset_button_clicked()

# ----------- grid toggle button ----------

grid_toggle_button = w.ToggleButton(
    value=False,
    description='Grid',
    disabled=False,
    button_style='',
    tooltip='Turn grid on',
    layout=w.Layout(width='auto')
)

def grid_toggle_button_clicked():
    with log_output:
        clear_output()
        #editor.reset()
        print_output('Grid visible!')
        time.sleep(3)
        clear_output()

@reset_button.on_click
def reset_on_click(b):
    reset_button_clicked()

# ----------- grid toggle button REAL ----------

box = w.Checkbox(False, description='Grid')