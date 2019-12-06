# external modules
import ipywidgets as w

# project-level modules
from ..settings import DEFAULT_FUNCTIONS, DEFAULT_FUNCTION_TO_SHOW


DEFAULT_DESCRIPTION_LENGTH = '120px'

# ----------- checkbox grid UNUSED ----------

checkbox_grid = w.Checkbox(False, description='Grid')

# ----------- checkbox color UNUSED ----------

checkbox_color = w.Checkbox(False, description='Red color')

# ----------- dropdown functions ----------

dropdown_functions = w.Dropdown(
    options=['user function'] + list(DEFAULT_FUNCTIONS.keys()),
    value='user function',
    description='Functions:',
    disabled=False,
    layout=w.Layout(width='auto', height='auto'),
    style={'description_width': DEFAULT_DESCRIPTION_LENGTH}
)

dropdown_functions_not_defined = w.Dropdown(
    options=DEFAULT_FUNCTIONS.keys(),
    value=DEFAULT_FUNCTION_TO_SHOW,
    description='Function:',
    disabled=False,
    layout=w.Layout(width='auto', height='auto'),
    style={'description_width': DEFAULT_DESCRIPTION_LENGTH}
)

# ----------- dropdown grid ----------

dropdown_grid = w.Dropdown(
    options=['false', 'true'],
    value='false',
    description='Grid visible:',
    disabled=False,
    layout=w.Layout(width='auto', height='auto'),
    style={'description_width': DEFAULT_DESCRIPTION_LENGTH}
)

# ----------- dropdown first derivative ----------

dropdown_derivative1 = w.Dropdown(
    options=['false', 'true'],
    value='false',
    description='1st derivative:',
    disabled=False,
    layout=w.Layout(width='auto', height='auto'),
    style={'description_width': DEFAULT_DESCRIPTION_LENGTH}
)

# ----------- dropdown second derivative ----------

dropdown_derivative2 = w.Dropdown(
    options=['false', 'true'],
    value='false',
    description='2nd derivative:',
    disabled=False,
    layout=w.Layout(width='auto', height='auto'),
    style={'description_width': DEFAULT_DESCRIPTION_LENGTH}
)

# ----------- dropdown third derivative ----------

dropdown_derivative3 = w.Dropdown(
    options=['false', 'true'],
    value='false',
    description='3rd derivative:',
    disabled=False,
    layout=w.Layout(width='auto', height='auto'),
    style={'description_width': DEFAULT_DESCRIPTION_LENGTH}
)

# ----------- color picker ----------

color_picker = w.ColorPicker(
    concise=False,
    description='Main line color:',
    value='#1f77b4',
    layout=w.Layout(width='auto', height='auto'),
    disabled=False,
    style={'description_width': DEFAULT_DESCRIPTION_LENGTH}
)

# ----------- refinement slider ----------

# refinement_slider = w.IntSlider(
#     value=0,
#     min=0,
#     max=3,
#     step=1,
#     description='Refinement:',
#     disabled=False,
#     continuous_update=False,
#     orientation='horizontal',
#     readout=True,
#     readout_format='d',
#     style={'description_width': DEFAULT_DESCRIPTION_LENGTH},
#     layout=w.Layout(width='auto', height='auto')
# )

dropdown_refinement = w.Dropdown(
    options=['original', '10x', '100x', '1000x', '10000x'],
    value='original',
    description='Refinement:',
    disabled=False,
    layout=w.Layout(width='auto', height='auto'),
    style={'description_width': DEFAULT_DESCRIPTION_LENGTH}
)