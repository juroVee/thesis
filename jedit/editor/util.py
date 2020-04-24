"""
JEDIT, editor which allows interactive exploration of the properties of elementary
functions in the computing environment IPython/Jupyter
Copyright (C) 2020 Juraj Vetrák

This file is part of JEDIT, editor which allows interactive
exploration of the properties of elementary functions in the computing environment IPython/Jupyter.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program (license.txt).  If not, see https://www.gnu.org/licenses/agpl-3.0.html.
"""

from IPython.display import display, HTML


def hide_interactive_toolbars():
    """
    Skryje na úrovni CSS interaktívne prvky v notebooku, ktoré narúšajú celkový vizuál aplikácie a nie sú podstatné.
    :return:
    """
    html = '''
            <style>
            .output_wrapper button.btn.btn-default,
            .output_wrapper .ui-dialog-titlebar,
            .output_wrapper .mpl-message,
            .output_wrapper .ui-icon {
              display: none!important;
            }
            </style>
           '''
    display(HTML(html))


def check_parameters(params, logger) -> dict:
    """
    Prekontroluje užívateľský vstup, zadané parametre, ich formát a hodnoty.
    :param params: užívateľské prametre
    :param logger: referencia na objektu Logger, pre prípadný výpis upozornení
    :return:
    """
    allowed_params = {'figure', 'axes', 'function', 'intervals', 'primes', 'asymptotes', 'config'}
    result = {}
    if len(params) == 0:
        return result
    for param in params.keys():
        if param not in allowed_params:
            logger.write(
                logger.new_message('Chyba', neznámy_parameter=param, akcia='vykreslenie prednastavenej funkcie'),
                mini=True)
            return result
    if any(param not in params for param in ['figure', 'axes', 'function', 'intervals']):
        logger.write(
            logger.new_message(
                'Parameters "figure", "axes", "function" and "intervals" are required to analysis your function.\nPlotting default.'),
            mini=True)
        return result
    else:
        others = {k: params[k] for k in set(params) - {'figure', 'axes', 'function'}}
        for param, value in others.items():
            if param == 'X':
                for i, X in enumerate(value):
                    if len(X) < 2:
                        logger.write(logger.new_message(
                            f'Cannot analysis X at position {i}, need at least 2 values.\nPlotting default.'),
                                     mini=True)
                        return result
            if type(value) != list:
                logger.write(logger.new_message(
                    'Optional parameters must be in list. E.g. intervals=[X1, ...].\nPlotting default.'),
                             mini=True)
                return result
    return params
