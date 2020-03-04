# external modules
import ipywidgets as w
from traitlets import directional_link
from collections import defaultdict

# project-level modules
from ..config import config


class GUIElementManager:


    def __init__(self, manager=None):
        self.manager = manager
        self.user_defined = manager.has_user_function()
        self.elements = defaultdict(dict)
        self.rules = {'vypnuté': True, 'zapnuté': False}
        self.name_length = 12
        self._init_hboxes()
        self._init_dropdowns()
        self._init_texts()

    def get_elements(self):
        return self.elements

    def _init_hboxes(self):
        self.elements['hbox']['function'] = self._function_hbox()
        for n in range(1, 4):
            self.elements['hbox'][f'derivative{n}'] = self._derivative_hbox(n)
        self.elements['hbox']['zero_points'] = self._zero_points_hbox_and_dropdown()[0]
        self.elements['hbox']['extremes'] = self._extremes_hbox_and_dropdown()
        self.elements['hbox']['inflex_points'] = self._inflex_points_hbox_and_dropdown()

    def _init_dropdowns(self):
        self.elements['dropdown']['grid'] = self._grid_dropdown()
        self.elements['dropdown']['refinement'] = self._refinement_dropdown()

    def _init_texts(self):
        self.elements['text']['zp_iterations'] = self._zero_points_hbox_and_dropdown()[1]

    def _function_hbox(self):
        default_color = config['main_function']['color']
        functions_names = [parameters['name'] for func, parameters in config['default_functions'].items()]
        default_function = config['main_function']['default']
        dropdown = w.Dropdown(
            options=['užívateľ'] + functions_names if self.user_defined else functions_names,
            value='užívateľ' if self.user_defined else config['default_functions'][default_function]['name'],
            description='Funkcia:',
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
        return w.HBox(children=[dropdown, cpicker], layout=w.Layout(overflow='hidden'))


    def _grid_dropdown(self):
        return w.Dropdown(
            options=['vypnuté', 'zapnuté'],
            value='vypnuté',
            description='Mriežka:',
            disabled=False,
            layout=w.Layout(width='auto', overflow='hidden'),
            style={'description_width': config['default_sizes']['menu_element_description']}
        )

    def _derivative_hbox(self, n=1):
        default_color = config['derivative']['colors'][n-1]
        dropdown = w.Dropdown(
            options=['vypnuté', 'zapnuté'],
            value='vypnuté',
            description=f'{n}.' + ' derivácia:',
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

        directional_link((dropdown, 'value'), (cpicker, 'disabled'), lambda case: self.rules[case])

        return w.HBox(children=[dropdown, cpicker], layout=w.Layout(overflow='hidden'))

    def _refinement_dropdown(self):
        return w.Dropdown(
            options=['pôvodné'] + [str(value) + 'x' for value in config['refinement']['values']],
            value='pôvodné',
            description='Zjemnenie:',
            disabled=False,
            layout=w.Layout(width='auto', overflow='hidden'),
            style={'description_width': config['default_sizes']['menu_element_description']}
        )

    def _zero_points_hbox_and_dropdown(self):
        default_color = config['zero_points']['color']
        dropdown = w.Dropdown(
            options=['vypnuté', 'zapnuté'],
            value='vypnuté',
            description='Nulové body:',
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
        iter_text = w.BoundedIntText(
            value=config['zero_points']['iterations'],
            min=1,
            max=1000,
            step=1,
            description='Iterácie:',
            disabled=False,
            layout=w.Layout(width='auto', overflow='hidden'),
            style={'description_width': config['default_sizes']['menu_element_description']}
        )

        directional_link((dropdown, 'value'), (cpicker, 'disabled'), lambda case: self.rules[case])

        return w.HBox(children=[dropdown, cpicker], layout=w.Layout(overflow='hidden')), iter_text

    def _extremes_hbox_and_dropdown(self):
        default_color = config['extremes']['color']
        dropdown = w.Dropdown(
            options=['vypnuté', 'zapnuté'],
            value='vypnuté',
            description='Extrémy:',
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

        directional_link((dropdown, 'value'), (cpicker, 'disabled'), lambda case: self.rules[case])

        return w.HBox(children=[dropdown, cpicker], layout=w.Layout(overflow='hidden'))

    def _inflex_points_hbox_and_dropdown(self):
        default_color = config['inflex_points']['color']
        dropdown = w.Dropdown(
            options=['vypnuté', 'zapnuté'],
            value='vypnuté',
            description='Inflexné body:',
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
        directional_link((dropdown, 'value'), (cpicker, 'disabled'), lambda case: self.rules[case])

        return w.Box(children=[dropdown, cpicker], layout=w.Layout(overflow='hidden'))