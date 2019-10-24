import ipywidgets as w
from ..config import DEFAULT_FUNCTIONS

# ----------- checkbox grid UNUSED ----------

checkbox_grid = w.Checkbox(False, description='Grid')

# ----------- checkbox color UNUSED ----------

checkbox_color = w.Checkbox(False, description='Red color')

# ----------- dropdown functions ----------

dropdown_functions = w.Dropdown(
    options=['user defined'] + list(DEFAULT_FUNCTIONS.keys()),
    value='user defined',
    description='Functions:',
    disabled=False,
    layout=w.Layout(width='auto', height='auto')
)

dropdown_functions_not_defined = w.Dropdown(
    options=DEFAULT_FUNCTIONS.keys(),
    value='y = x',
    description='Functions:',
    disabled=False,
    layout=w.Layout(width='auto', height='auto')
)

# ----------- dropdown grid ----------

dropdown_grid = w.Dropdown(
    options=['False', 'True'],
    value='False',
    description='Grid:',
    disabled=False,
    layout=w.Layout(width='auto', height='auto')
)

# ----------- color picker ----------

color_picker = w.ColorPicker(
    concise=False,
    description='Line color:',
    value='#1f77b4',
    layout=w.Layout(width='auto', height='auto'),
    disabled=False
)

# ----------- freq slider UNUSED ----------

freq_slider = w.FloatSlider(
        value=2.,
        min=1.,
        max=10.0,
        step=0.1,
        description='Frequency:',
        readout_format='.1f')

# ----------- range slider UNUSED ----------

range_slider = w.FloatRangeSlider(
        value=[-1., +1.],
        min= -5., max= +5., step=0.1,
        description='xlim:',
        readout_format='.1f')