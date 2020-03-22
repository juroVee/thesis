# external modules
from IPython.display import display, HTML
import numpy as np


def logger_message(theme, **kwargs):
    return theme, kwargs

def transform_title(title: str) -> str:
    if title == '':
        return ''
    start = title.find('$')
    end = title.rfind('$')
    result = r'' + title[start:end + 1]
    return result

def check_parameters(params, logger) -> dict:
    allowed_params = {'fig', 'ax', 'f', 'X', 'Y', 'fprimes', 'asymptotes', 'config'}
    result = {}
    if len(params) == 0:
        return result
    for param in params.keys():
        if param not in allowed_params:
            logger.write(logger_message('Chyba', neznámy_parameter=param, akcia='vykreslenie prednastavenej funkcie'), mini=True)
            return result
    if any(param not in params for param in ['fig', 'ax', 'f', 'X']):
        logger.write('Parameters [fig, ax, f, X] are required to plot your function.\nPlotting default.', mini=True)
        return result
    else:
        others = { k : params[k] for k in set(params) - {'fig', 'ax', 'f'} }
        for param, value in others.items():
            if param == 'X':
                for i, X in enumerate(value):
                    if len(X) < 2:
                        logger.write(f'Cannot plot X at position {i}, need at least 2 values.\nPlotting default.', mini=True)
                        return result
            if type(value) != list:
                logger.write('Optional parameters must be in list. E.g. X=[X, ...].\nPlotting default.', mini=True)
                return result
    return params

def flatten(dataset, params=None, full=False):
    if params is not None:
        result = []
        for param in params:
            result.append(np.sort(np.asarray([dct[param] for dct in dataset.values()]).flatten()))
        if full:
            result.append(np.sort(np.concatenate(result)))
        return result
    return np.asarray([arr for arr in dataset.values()]).flatten()

def hide_interactive_toolbars():
    html = '''
            <style>
            .output_wrapper button.btn.btn-default,
            .output_wrapper .ui-dialog-titlebar,
            .output_wrapper .mpl-message {
              display: none;
            }
            </style>
           '''
    display(HTML(html))