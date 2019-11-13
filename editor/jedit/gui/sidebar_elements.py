import ipywidgets as w
from ..config.settings import DEFAULT_FUNCTIONS, DEFAULT_FUNCTION_TO_SHOW

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

# ----------- dropdown grid ----------

dropdown_derivative = w.Dropdown(
    options=['none'] + [f'n = {i}' for i in range(1, 6)],
    value='none',
    description='Derivative:',
    disabled=False,
    layout=w.Layout(width='auto', height='auto'),
    style={'description_width': DEFAULT_DESCRIPTION_LENGTH}
)

# ----------- color picker ----------

color_picker = w.ColorPicker(
    concise=False,
    description='Line color:',
    value='#1f77b4',
    layout=w.Layout(width='auto', height='auto'),
    disabled=False,
    style={'description_width': DEFAULT_DESCRIPTION_LENGTH}
)

# ----------- freq slider UNUSED ----------

refinement_slider = w.FloatSlider(
        value=0.,
        min=0.,
        max=2.0,
        step=0.1,
        description='Refinement:',
        readout_format='.1f',
        continuous_update=False,
        layout=w.Layout(width='auto', height='auto')
)

# ----------- range slider ----------

range_slider = w.FloatRangeSlider(
        value=[-10., +10.],
        min= -20., max= +20., step=0.1,
        description='X Range:',
        continuous_update=False,
        readout_format='.1f',
        orientation='horizontal',
        layout=w.Layout(width='auto', height='auto')
)