import ipywidgets as w
from ..config.settings import DEFAULT_FUNCTIONS, DEFAULT_FUNCTION_SHOW

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
    value=DEFAULT_FUNCTION_SHOW,
    description='Functions:',
    disabled=False,
    layout=w.Layout(width='auto', height='auto')
)

# ----------- dropdown grid ----------

dropdown_grid = w.Dropdown(
    options=['false', 'true'],
    value='false',
    description='Grid:',
    disabled=False,
    layout=w.Layout(width='auto', height='auto')
)

# ----------- dropdown aspect ----------

dropdown_aspect = w.Dropdown(
    options=['auto', 'equal'],
    value='auto',
    description='Aspect:',
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