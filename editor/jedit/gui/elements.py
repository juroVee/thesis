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
        self.main_menu = self._init_menu()

    def get_elements(self):
        return self.elements

    def get_main_menu(self):
        return self.main_menu

    def _init_menu(self):
        tab_function_grid = w.GridspecLayout(config['default_sizes']['main_window_rows'] - 2, 1)
        tab_function_grid[0, 0] = self.elements['function']['function'] = self._function_hbox()
        tab_function_grid[1, 0] = self.elements['function']['grid'] = self._grid_dropdown()
        tab_function_grid[3, 0] = self.elements['function']['derivative1'] = self._derivative_hbox(1)
        tab_function_grid[4, 0] = self.elements['function']['derivative2'] = self._derivative_hbox(2)
        tab_function_grid[5, 0] = self.elements['function']['derivative3'] = self._derivative_hbox(3)

        tab_analysis_grid = w.GridspecLayout(config['default_sizes']['main_window_rows'] - 2, 1)
        tab_analysis_grid[0, 0] = self.elements['analysis']['refinement'] = self._refinement_dropdown()
        tab_analysis_grid[1, 0] = self.elements['analysis']['iterations'] = self._zero_points_hbox_and_dropdown()[1]
        tab_analysis_grid[3, 0] = self.elements['analysis']['zero_points'] = self._zero_points_hbox_and_dropdown()[0]
        tab_analysis_grid[4, 0] = self.elements['analysis']['extremes'] = self._extremes_hbox_and_dropdown()
        tab_analysis_grid[5, 0] = self.elements['analysis']['inflex_points'] = self._inflex_points_hbox_and_dropdown()

        tab_nest = w.Tab()
        tab_nest.children = [tab_function_grid, tab_analysis_grid]
        tab_nest.set_title(0, 'Funkcia')
        tab_nest.set_title(1, 'Analýza')
        return tab_nest

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