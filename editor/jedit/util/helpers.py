from .custom_errors import MissingParameterException
from IPython.display import display, HTML
import random, string

N_PARAMETERS = 4

def transform_title(title: str) -> str:
    if title == '':
        return 'f(x)'
    start = title.find('$')
    end = title.rfind('$')
    result = r'' + title[start:end + 1]
    if 'y' in result:
        result = result.replace('y', 'f(x)')
    return result

def get_user_parameters(fig, ax, func, xvals) -> dict:
    number_of_missing_parameters = check_params(fig, ax, func, xvals)
    if number_of_missing_parameters == N_PARAMETERS:
        return None
    return {
        'figure': fig,
        'axis': ax,
        'function': func,
        'xvals': xvals
    }

def check_params(fig, ax, f, X):
    missing = []
    for name, var in zip(['figure', 'axis', 'function'], [fig, ax, f]):
        if var is None:
            missing.append(name)
    if len(X) == 0:
        missing.append('X_values')
    if 0 < len(missing) < N_PARAMETERS:
        raise MissingParameterException('Not all parameters entered. Enter all parameters or none at all.\n\t'
                                        f'Missing parameters: {missing}')
    return len(missing)

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