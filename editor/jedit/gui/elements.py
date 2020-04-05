import ipywidgets as w
from traitlets import directional_link


class HBox:

    def __init__(self, description, disabled, color, link=False):
        self.description = description
        self.disabled = disabled
        self.color = color
        self.link = link

    def get(self):
        toggle = w.ToggleButton(
            value=False,
            description=self.description,
            disabled=self.disabled,
            button_style='',
            tooltip='Description',
            layout=w.Layout(width='90%', border='1px solid darkgrey')
        )
        cpicker = w.ColorPicker(
            concise=True,
            description='',
            value=self.color,
            disabled=False,
            layout=w.Layout(width='28px')
        )
        if self.link:
            directional_link((toggle, 'value'), (cpicker, 'disabled'), lambda case: not case)
        return w.HBox(children=[toggle, cpicker], layout=w.Layout(overflow='hidden', border='1px solid darkgrey'))


class Toggle:

    def __init__(self, description, disabled):
        self.description = description
        self.disabled = disabled

    def get(self):
        toggle = w.ToggleButton(
            value=False,
            description=self.description,
            disabled=self.disabled,
            button_style='',
            tooltip='Description',
            layout=w.Layout(width='100%', border='1px solid darkgrey')
        )
        return w.HBox(children=[toggle], layout=w.Layout(overflow='hidden', border='1px solid darkgrey'))


class Dropdown:

    def __init__(self, description, disabled, values, default_value):
        self.description = description
        self.disabled = disabled
        self.values = values
        self.default_value = default_value

    def get(self):
        toggle = w.ToggleButton(
            value=False,
            description=self.description,
            disabled=True,
            button_style='',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Description',
            layout=w.Layout(width='90%', border='1px solid darkgrey')
        )
        dropdown = w.Dropdown(
            options=self.values,
            value=self.default_value,
            description='',
            disabled=self.disabled,
            layout=w.Layout(width='100%', overflow='hidden')
        )
        return w.HBox(children=[toggle, dropdown], layout=w.Layout(overflow='hidden', border='1px solid darkgrey'))


class Text:

    def __init__(self, description, disabled, minval, maxval, step, default_value):
        self.description = description
        self.disabled = disabled
        self.min = minval
        self.max = maxval
        self.step = step
        self.default_value = default_value

    def get(self):
        toggle = w.ToggleButton(
            value=False,
            description=self.description,
            disabled=True,
            button_style='',
            tooltip='Description',
            layout=w.Layout(width='90%', border='1px solid darkgrey')
        )
        textfield = w.BoundedIntText(
            value=self.default_value,
            min=self.min,
            max=self.max,
            step=self.step,
            description='',
            disabled=self.disabled,
            layout=w.Layout(width='100%', overflow='hidden')
        )
        return w.HBox(children=[toggle, textfield], layout=w.Layout(overflow='hidden', border='1px solid darkgrey'))


class Button:

    def __init__(self, description, disabled):
        self.description = description
        self.disabled = disabled

    def get(self):
        button = w.Button(
            value=False,
            description=self.description,
            disabled=self.disabled,
            button_style='',
            tooltip='Description',
            layout=w.Layout(width='100%', border='1px solid darkgrey')
        )
        return w.HBox(children=[button], layout=w.Layout(overflow='hidden', border='1px solid darkgrey'))