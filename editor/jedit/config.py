from .editor import Editor
from IPython.display import display, HTML

editor = Editor()

display(HTML('''
    <style>
    .cell .output_wrapper .ui-dialog-titlebar {
      display: none;
    }    
    </style>
'''))