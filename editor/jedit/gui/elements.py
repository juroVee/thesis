# external modules
import ipywidgets as w
from traitlets import directional_link

# project-level modules
from ..config import config


class GUIElementManager:


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
            self.elements[f'hbox_derivative{n}'] = self._derivative_hbox(n)
        self.elements['dropdown_refinement'] = self._refinement_dropdown()
        self.elements['hbox_zero_points'] = self._zero_points_hbox()

    def _function_hbox(self):
        default_color = config['main_function']['color']
        functions_names = [parameters['name'] for func, parameters in config['default_functions'].items()]
        default_function = config['main_function']['default']
        dropdown = w.Dropdown(
            options=['user function'] + functions_names if self.user_defined else functions_names,
            value='user function' if self.user_defined else config['default_functions'][default_function]['name'],
            description='Function:',
            disabled=False,
            layout=w.Layout(width='100%'),
            style={'description_width': config['default_sizes']['menu_element_description']}
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
            style={'description_width': config['default_sizes']['menu_element_description']}
        )

    def _derivative_hbox(self, n=1):
        default_color = config['derivative']['colors'][n-1]
        dropdown = w.Dropdown(
            options=['false', 'true'],
            value='false',
            description=f'{n}.' + ' derivative:',
            disabled=False,
            layout=w.Layout(width='100%'),
            style={'description_width': config['default_sizes']['menu_element_description']}
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
            options=['original'] + [str(value) + 'x' for value in config['refinement']['values']],
            value='original',
            description='Refinement:',
            disabled=False,
            layout=w.Layout(width='auto', height='auto'),
            style={'description_width': config['default_sizes']['menu_element_description']}
        )

    def _zero_points_hbox(self):
        default_color = config['zero_points']['color']
        dropdown = w.Dropdown(
            options=['none', 'newton', 'brentq', 'bisect'],
            value='none',
            description='Zero points:',
            disabled=False,
            layout=w.Layout(width='100%'),
            style={'description_width': config['default_sizes']['menu_element_description']}
        )
        cpicker = w.ColorPicker(
            concise=True,
            description='',
            value=default_color,
            disabled=False,
            layout=w.Layout(width='28px')
        )

        directional_link((dropdown, 'value'), (cpicker, 'disabled'), lambda case: True if case == 'none' else False)

        return w.HBox(children=[dropdown, cpicker])