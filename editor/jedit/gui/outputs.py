from .output import Output

def print_output(text):
    print(text)

# Widget for displaying logs at the bottom left of the editor
log_output = Output().get_widget()