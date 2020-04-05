# external modules
from IPython.display import display, HTML


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
    allowed_params = {'figure', 'axes', 'function', 'intervals', 'primes', 'asymptotes', 'config'}
    result = {}
    if len(params) == 0:
        return result
    for param in params.keys():
        if param not in allowed_params:
            logger.write(logger_message('Chyba', neznámy_parameter=param, akcia='vykreslenie prednastavenej funkcie'), mini=True)
            return result
    if any(param not in params for param in ['figure', 'axes', 'function', 'intervals']):
        logger.write('Parameters "figure", "axes", "function" and "intervals" are required to plot your function.\nPlotting default.', mini=True)
        return result
    else:
        others = { k : params[k] for k in set(params) - {'figure', 'axes', 'function'} }
        for param, value in others.items():
            if param == 'X':
                for i, X in enumerate(value):
                    if len(X) < 2:
                        logger.write(f'Cannot plot X at position {i}, need at least 2 values.\nPlotting default.', mini=True)
                        return result
            if type(value) != list:
                logger.write('Optional parameters must be in list. E.g. intervals=[X1, ...].\nPlotting default.', mini=True)
                return result
    return params

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