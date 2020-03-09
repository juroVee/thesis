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
        tab_function_grid = w.GridspecLayout(config['default_sizes']['main_window_rows'] - 4, 1)
        tab_function_grid[0, 0] = self.elements['function']['function'] = self.get_function_hbox()
        tab_function_grid[2, 0] = self.elements['function']['grid'] = self.get_grid_dropdown()
        tab_function_grid[3, 0] = self.elements['function']['aspect'] = self.get_button_aspect()
        tab_function_grid[5, 0] = self.elements['function']['derivative1'] = self.get_derivative_hbox(1)
        tab_function_grid[6, 0] = self.elements['function']['derivative2'] = self.get_derivative_hbox(2)
        tab_function_grid[7, 0] = self.elements['function']['derivative3'] = self.get_derivative_hbox(3)

        tab_analysis_grid = w.GridspecLayout(config['default_sizes']['main_window_rows'] - 4, 1)
        tab_analysis_grid[0, 0] = self.elements['analysis']['zero_points'] = self.get_analysis_hbox(op='zero_points')
        tab_analysis_grid[1, 0] = self.elements['analysis']['extremes'] = self.get_analysis_hbox(op='extremes')
        tab_analysis_grid[2, 0] = self.elements['analysis']['inflex_points'] = self.get_analysis_hbox(op='inflex_points')
        tab_analysis_grid[4, 0] = self.elements['analysis']['increasing'] = self.get_analysis_hbox(op='increasing')
        tab_analysis_grid[5, 0] = self.elements['analysis']['decreasing'] = self.get_analysis_hbox(op='decreasing')
        tab_analysis_grid[6, 0] = self.elements['analysis']['convex'] = self.get_analysis_hbox(op='convex')
        tab_analysis_grid[7, 0] = self.elements['analysis']['concave'] = self.get_analysis_hbox(op='concave')
        tab_analysis_grid[9, 0] = self.elements['analysis']['refinement'] = self.get_refinement_dropdown()
        tab_analysis_grid[10, 0] = self.elements['analysis']['iterations'] = self.get_iterations_textfield()

        tab_nest = w.Tab()
        tab_nest.children = [tab_analysis_grid, tab_function_grid]
        tab_nest.set_title(0, 'Analýza')
        tab_nest.set_title(1, 'Možnosti')
        return tab_nest

    def get_function_hbox(self):
        default_color = config['main_function']['color']
        functions_names = [parameters['name'] for func, parameters in config['default_functions'].items()]
        default_function = config['main_function']['default']
        button = w.ToggleButton(
            value=False,
            description='Funkcia',
            disabled=True,
            button_style='',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Description',
            layout=w.Layout(width='90%', border='1px solid darkgrey')
        )
        dropdown = w.Dropdown(
            options=['užívateľ'] + functions_names if self.user_defined else functions_names,
            value='užívateľ' if self.user_defined else config['default_functions'][default_function]['name'],
            description='',
            disabled=False,
            layout=w.Layout(width='100%')
        )
        cpicker = w.ColorPicker(
            concise=True,
            description='',
            value=default_color,
            disabled=False,
            layout=w.Layout(width='28px')
        )
        return w.HBox(children=[button, dropdown, cpicker], layout=w.Layout(overflow='hidden', border='1px solid darkgrey'))


    def get_grid_dropdown(self):
        grid_button = w.ToggleButton(
            value=False,
            description=f'Mriežka',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Description',
            layout=w.Layout(width='100%', border='1px solid darkgrey')
        )
        return w.HBox(children=[grid_button], layout=w.Layout(overflow='hidden', border='1px solid darkgrey'))

    def get_button_aspect(self):
        current_function = self.manager.get_current()
        default = current_function.get_parameter('aspect')
        button = w.ToggleButton(
            value=False,
            description='Aspekt',
            disabled=True,
            button_style='',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Description',
            layout=w.Layout(width='90%', border='1px solid darkgrey')
        )
        dropdown = w.Dropdown(
            options=['automatický', 'vyrovnaný'],
            value='automatický' if default == 'auto' else 'vyrovnaný',
            description='',
            disabled=False,
            layout=w.Layout(width='100%', overflow='hidden')
        )
        return w.HBox(children=[button, dropdown], layout=w.Layout(overflow='hidden', border='1px solid darkgrey'))

    def get_derivative_hbox(self, n=1):
        default_color = config['derivative']['colors'][n-1]
        button = w.ToggleButton(
            value=False,
            description=f'{n}.' + ' derivácia',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Description',
            layout=w.Layout(width='90%', border='1px solid darkgrey')
        )
        cpicker = w.ColorPicker(
            concise=True,
            description='',
            value=default_color,
            disabled=False,
            layout=w.Layout(width='28px')
        )
        directional_link((button, 'value'), (cpicker, 'disabled'), lambda case: not case)
        return w.HBox(children=[button, cpicker], layout=w.Layout(overflow='hidden', border='1px solid darkgrey'))

    def get_refinement_dropdown(self):
        button = w.ToggleButton(
            value=False,
            description='Zjemnenie',
            disabled=True,
            button_style='',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Description',
            layout=w.Layout(width='90%', border='1px solid darkgrey')
        )
        dropdown = w.Dropdown(
            options=['pôvodné'] + [str(value) + 'x' for value in config['refinement']['values']],
            value='pôvodné',
            description='',
            disabled=False,
            layout=w.Layout(width='100%', overflow='hidden')
        )
        return w.HBox(children=[button, dropdown], layout=w.Layout(overflow='hidden', border='1px solid darkgrey'))

    def get_iterations_textfield(self):
        button = w.ToggleButton(
            value=False,
            description='Iterácie',
            disabled=True,
            button_style='',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Description',
            layout=w.Layout(width='90%', border='1px solid darkgrey')
        )
        textfield = w.BoundedIntText(
            value=config['zero_points']['iterations'],
            min=1,
            max=1000,
            step=1,
            description='',
            disabled=False,
            layout=w.Layout(width='100%', overflow='hidden')
        )
        return w.HBox(children=[button, textfield], layout=w.Layout(overflow='hidden', border='1px solid darkgrey'))

    def get_analysis_hbox(self, op='zero_points'):
        default_color = config[op]['color']
        descriptions = {'zero_points': 'Nulové body',
                        'extremes': 'Ostré lokálne extrémy',
                        'inflex_points': 'Inflexné body',
                        'increasing': 'Rastúca',
                        'decreasing': 'Klesajúca',
                        'convex': 'Konvexná',
                        'concave': 'Konkávna'}
        button = w.ToggleButton(
            value=False,
            description=f'{descriptions[op]}',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Description',
            layout=w.Layout(width='90%', border='1px solid darkgrey')
        )
        cpicker = w.ColorPicker(
            concise=True,
            description='',
            value=default_color,
            disabled=False,
            layout=w.Layout(width='28px')
        )
        directional_link((button, 'value'), (cpicker, 'disabled'), lambda case: not case)
        return w.HBox(children=[button, cpicker], layout=w.Layout(overflow='hidden', border='1px solid darkgray'))