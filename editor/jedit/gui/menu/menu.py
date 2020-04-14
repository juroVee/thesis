from collections import defaultdict

import ipywidgets as w

from .elements import HBox, Dropdown, Text, Toggle, Button
from ...config import config


class MainMenu:

    def __init__(self):
        self.elements = defaultdict(dict)
        self._init_menu()

    def _init_menu(self):
        """
        Vytvorí a vráti mriežkové štruktúry pre uloženie ovládacích prvkov, ktoré sú prístupné v objekte Tab.
        :return: Hlavné menu v podobe Tab objektu
        """
        a_grid = w.GridspecLayout(config['default_sizes']['main_window_rows'] - 4, 1)

        a_grid[0, 0] = self.elements['hbox']['zero_points'] = HBox(description='Nulové body',
                                                                   disabled=False,
                                                                   color=config['zero_points']['color'],
                                                                   link=True).get()

        a_grid[1, 0] = self.elements['hbox']['extremes'] = HBox(description='Ostré lokálne extrémy',
                                                                disabled=False,
                                                                color=config['extremes']['color'],
                                                                link=True).get()

        a_grid[2, 0] = self.elements['hbox']['inflex_points'] = HBox(description='Inflexné body',
                                                                     disabled=False,
                                                                     color=config['inflex_points']['color'],
                                                                     link=True).get()

        a_grid[4, 0] = self.elements['hbox']['increasing'] = HBox(description='Rastúca',
                                                                  disabled=False,
                                                                  color=config['increasing']['color'],
                                                                  link=True).get()

        a_grid[5, 0] = self.elements['hbox']['decreasing'] = HBox(description='Klesajúca',
                                                                  disabled=False,
                                                                  color=config['decreasing']['color'],
                                                                  link=True).get()

        a_grid[6, 0] = self.elements['hbox']['concave_up'] = HBox(description='Konvexná',
                                                                  disabled=False,
                                                                  color=config['concave_up']['color'],
                                                                  link=True).get()

        a_grid[7, 0] = self.elements['hbox']['concave_down'] = HBox(description='Konkávna',
                                                                    disabled=False,
                                                                    color=config['concave_down']['color'],
                                                                    link=True).get()

        a_grid[9, 0] = self.elements['dropdown']['refinement_x'] = Dropdown(description='Zjemnenie osi x',
                                                                            disabled=False,
                                                                            values=list(map(lambda
                                                                                                n: n + 'x' if n != 'pôvodné' else n,
                                                                                            config['refinement_x'][
                                                                                                'values'])),
                                                                            default_value='pôvodné').get()

        a_grid[10, 0] = self.elements['dropdown']['rounding'] = Dropdown(description='Zaokrúhlenie hodnôt',
                                                                         disabled=False,
                                                                         values=list(range(
                                                                             config['editor_settings']['round']['to'],
                                                                             config['editor_settings']['round'][
                                                                                 'from'] - 1, -1)),
                                                                         default_value=
                                                                         config['editor_settings']['round'][
                                                                             'default']).get()

        a_grid[12, 0] = self.elements['text']['iterations'] = Text(description='Iterácie Newtonovej metódy',
                                                                   disabled=False,
                                                                   minval=1,
                                                                   maxval=1000,
                                                                   step=1,
                                                                   default_value=config['zero_points'][
                                                                       'iterations']).get()

        f_grid = w.GridspecLayout(config['default_sizes']['main_window_rows'] - 7, 1)

        f_grid[0, 0] = self.elements['hbox']['main_function'] = HBox(description='Funkcia',
                                                                     disabled=True,
                                                                     color=config['main_function']['color']).get()

        f_grid[2, 0] = self.elements['hbox']['derivative1'] = HBox(description='1. derivácia',
                                                                   disabled=False,
                                                                   color=config['derivative']['colors'][0]).get()

        f_grid[3, 0] = self.elements['hbox']['derivative2'] = HBox(description='2. derivácia',
                                                                   disabled=False,
                                                                   color=config['derivative']['colors'][1]).get()

        f_grid[4, 0] = self.elements['hbox']['derivative3'] = HBox(description='3. derivácia',
                                                                   disabled=False,
                                                                   color=config['derivative']['colors'][2]).get()

        f_grid[6, 0] = self.elements['toggle']['grid'] = Toggle(description='Mriežka',
                                                                disabled=False).get()

        f_grid[8, 0] = self.elements['dropdown']['logger_order'] = Dropdown(description='Poradie výpisov',
                                                                            disabled=False,
                                                                            values=['najnovšie',
                                                                                    'najstaršie'],
                                                                            default_value='najnovšie').get()

        f_grid[9, 0] = self.elements['button']['logger_save'] = Button(description='Uložiť výpisy do súboru',
                                                                       disabled=False).get()

        tab_nest = w.Tab()
        tab_nest.children = [a_grid, f_grid]
        tab_nest.set_title(0, 'Analýza')
        tab_nest.set_title(1, 'Možnosti')
        self.main_menu = tab_nest

    def get_elements(self) -> defaultdict:
        """
        :return: Slovník všetkých prvkov menu pre rýchly prístup.
        """
        return self.elements

    def get_widget(self) -> w.Tab:
        """
        :return: Hlavné menu v podobe Tab objektu
        """
        return self.main_menu