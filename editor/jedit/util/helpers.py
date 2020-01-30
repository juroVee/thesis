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
    allowed_params = {'fig', 'ax', 'f', 'X', 'Y', 'd', 'a'}
    result = {}
    if len(params) == 0:
        return result
    for param in params.keys():
        if param not in allowed_params:
            logger.write_mini(f'Unrecognized parameter "{param}".\nPlotting default.')
            return result
    if any(param not in params for param in ['fig', 'ax', 'f', 'X']):
        logger.write_mini('Parameters [fig, ax, f, X] are needed to plot your function.\nPlotting default.')
        return result
    else:
        others = { k : params[k] for k in set(params) - {'fig', 'ax', 'f'} }
        for param, value in others.items():
            if type(value) != list:
                logger.write_mini('Optional parameters must be in list. E.g. X=[X, ...].\nPlotting default.')
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