# external modules
from IPython.display import display, HTML


def transform_title(title: str) -> str:
    if title == '':
        return ''
    start = title.find('$')
    end = title.rfind('$')
    result = r'' + title[start:end + 1]
    return result

def check_parameters(params, logger) -> dict:
    allowed_params = {'fig', 'ax', 'f', 'X', 'Y', 'primes', 'asymptotes'}
    result = {}
    if len(params) == 0:
        return result
    for param in params.keys():
        if param not in allowed_params:
            logger.write(f'Unrecognized parameter "{param}".\nPlotting default.', mini=True)
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