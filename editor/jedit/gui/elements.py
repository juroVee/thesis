import ipywidgets as w
from traitlets import directional_link


class HBox:

    def __init__(self, description, disabled, color, link=False, tooltip=None):
        self.description = description
        self.disabled = disabled
        self.color = color
        self.link = link
        self.tooltip = tooltip

    def get(self):
        toggle = w.ToggleButton(
            value=False,
            description=self.description,
            disabled=self.disabled,
            button_style='',
            tooltip=self.tooltip if self.tooltip is not None else self.description,
            layout=w.Layout(width='90%')
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
        return w.HBox(children=[toggle, cpicker], layout=w.Layout(overflow='hidden'))


class Toggle:

    def __init__(self, description, disabled, tooltip=None):
        self.description = description
        self.disabled = disabled
        self.tooltip = tooltip

    def get(self):
        toggle = w.ToggleButton(
            value=False,
            description=self.description,
            disabled=self.disabled,
            button_style='',
            tooltip=self.tooltip if self.tooltip is not None else self.description,
            layout=w.Layout(width='100%')
        )
        return w.HBox(children=[toggle], layout=w.Layout(overflow='hidden'))


class Dropdown:

    def __init__(self, description, disabled, values, default_value, tooltip=None):
        self.description = description
        self.disabled = disabled
        self.values = values
        self.default_value = default_value
        self.tooltip = tooltip

    def get(self):
        toggle = w.ToggleButton(
            value=False,
            description=self.description,
            disabled=True,
            button_style='',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip=self.tooltip if self.tooltip is not None else self.description,
            layout=w.Layout(width='100%')
        )
        dropdown = w.Dropdown(
            options=self.values,
            value=self.default_value,
            description='',
            disabled=self.disabled,
            layout=w.Layout(width='70%', overflow='hidden')
        )
        return w.HBox(children=[toggle, dropdown], layout=w.Layout(overflow='hidden'))


class IntText:

    def __init__(self, description, disabled, minval, maxval, step, default_value, tooltip=None):
        self.description = description
        self.disabled = disabled
        self.min = minval
        self.max = maxval
        self.step = step
        self.default_value = default_value
        self.tooltip = tooltip

    def get(self):
        toggle = w.ToggleButton(
            value=False,
            description=self.description,
            disabled=True,
            button_style='',
            tooltip=self.tooltip if self.tooltip is not None else self.description,
            layout=w.Layout(width='100%')
        )
        textfield = w.BoundedIntText(
            value=self.default_value,
            min=self.min,
            max=self.max,
            step=self.step,
            description='',
            disabled=self.disabled,
            layout=w.Layout(width='40%', overflow='hidden')
        )
        return w.HBox(children=[toggle, textfield], layout=w.Layout(overflow='hidden'))


class Button:

    def __init__(self, description, disabled, tooltip=None):
        self.description = description
        self.disabled = disabled
        self.tooltip = tooltip

    def get(self):
        button = w.Button(
            value=False,
            description=self.description,
            disabled=self.disabled,
            button_style='',
            tooltip=self.tooltip if self.tooltip is not None else self.description,
            layout=w.Layout(width='100%')
        )
        return w.HBox(children=[button], layout=w.Layout(overflow='hidden'))
