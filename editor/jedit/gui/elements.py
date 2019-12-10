# external modules
import ipywidgets as w
from traitlets import directional_link

# project-level modules
from ..settings import DEFAULT_FUNCTIONS, DEFAULT_FUNCTION_TO_SHOW, DERIV_COLORS


class GUIElementManager:

    DEFAULT_DESCRIPTION_LENGTH = '120px'

    def __init__(self, user_defined=False):
        self.user_defined = user_defined
        self.elements = {}
        self._init_elements()

    def get_elements(self):
        return self.elements

    def _init_elements(self):
        self.elements['hbox_function'] = self._function_hbox()
        self.elements['dropdown_grid'] = self._grid_dropdown()
        for n in range(1, 4):
            self.elements[f'hbox_derivative{n}'] = self._derivative_hbox(n, DERIV_COLORS[n])
        self.elements['dropdown_refinement'] = self._refinement_dropdown()
        self.elements['hbox_zero_points'] = self._zero_points_hbox()

    def _function_hbox(self, default_color='#1f77b4'):
        dropdown = w.Dropdown(
            options=['user function'] + list(DEFAULT_FUNCTIONS.keys()) if self.user_defined else DEFAULT_FUNCTIONS.keys(),
            value='user function' if self.user_defined else DEFAULT_FUNCTION_TO_SHOW,
            description='Function:',
            disabled=False,
            layout=w.Layout(width='100%'),
            style={'description_width': self.DEFAULT_DESCRIPTION_LENGTH}
        )
        cpicker = w.ColorPicker(
            concise=True,
            description='',
            value=default_color,
            disabled=False,
            layout=w.Layout(width='28px')
        )
        return w.HBox(children=[dropdown, cpicker])


    def _grid_dropdown(self):
        return w.Dropdown(
            options=['false', 'true'],
            value='false',
            description='Grid:',
            disabled=False,
            layout=w.Layout(width='auto', height='auto'),
            style={'description_width': self.DEFAULT_DESCRIPTION_LENGTH}
        )

    def _derivative_hbox(self, n=1, default_color='#1f77b4'):
        dropdown = w.Dropdown(
            options=['false', 'true'],
            value='false',
            description=f'{n}.' + ' derivative:',
            disabled=False,
            layout=w.Layout(width='100%'),
            style={'description_width': self.DEFAULT_DESCRIPTION_LENGTH}
        )
        cpicker = w.ColorPicker(
            concise=True,
            description='',
            value=default_color,
            disabled=False,
            layout=w.Layout(width='28px')
        )

        def transform(case):
            return {'false': True, 'true': False}[case]

        directional_link((dropdown, 'value'), (cpicker, 'disabled'), transform)

        return w.HBox(children=[dropdown, cpicker])

    def _refinement_dropdown(self):
        return w.Dropdown(
            options=['original', '10x', '100x', '1000x', '10000x'],
            value='original',
            description='Refinement:',
            disabled=False,
            layout=w.Layout(width='auto', height='auto'),
            style={'description_width': self.DEFAULT_DESCRIPTION_LENGTH}
        )

    def _zero_points_hbox(self, default_color='#000000'):
        dropdown = w.Dropdown(
            options=['none', 'newton', 'brentq', 'bisect'],
            value='none',
            description='Zero points:',
            disabled=False,
            layout=w.Layout(width='100%'),
            style={'description_width': self.DEFAULT_DESCRIPTION_LENGTH}
        )
        cpicker = w.ColorPicker(
            concise=True,
            description='',
            value=default_color,
            disabled=False,
            layout=w.Layout(width='28px')
        )

        def transform(case):
            return True if case == 'none' else False

        directional_link((dropdown, 'value'), (cpicker, 'disabled'), transform)

        return w.HBox(children=[dropdown, cpicker])