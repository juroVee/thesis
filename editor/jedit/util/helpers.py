# package-level modules
from .custom_errors import MissingParameterException

# external modules
from IPython.display import display, HTML
import random, string

N_PARAMETERS = 4

def transform_title(title: str) -> str:
    if title == '':
        return ''
    start = title.find('$')
    end = title.rfind('$')
    result = r'' + title[start:end + 1]
    return result

def check_user_parameters(fig, ax, f, params, logger) -> dict:
    allowed_params = ['X', 'Y', 'derivatives', 'asymptotes']
    result = {}
    if all(value is not None for value in [fig, ax]):
        result = {'fig': fig, 'ax': ax, 'f': f}
        for param, value in params.items():
            if type(value) != list:
                logger.write_mini('Optional parameters must be in list. E.g. X=[X, ...]\n'
                                  + len('[LATEST] ') * ' ' + 'Plotting default functions.')
                return {}
            if param not in allowed_params:
                logger.write_mini(f'Unrecognized parameter {param}.\n'
                                  + len('[LATEST] ') * ' ' + 'Plotting default functions.')
            result[param] = value
    else:
        logger.write_mini('Parameters fig, ax and f must be specified.\n'
                          + len('[LATEST] ') * ' ' + 'Plotting default functions.')
    return result

def hide_interactive_toolbars():
    html = '''
            <style>
            .output_wrapper button.btn.btn-default,
            .output_wrapper .ui-dialog-titlebar {
              display: none;
            }
            </style>
        '''
    display(HTML(html))

def generate_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

def assign(var: str, code: str):
    return var + ' = ' + code