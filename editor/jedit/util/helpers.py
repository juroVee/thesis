from .custom_errors import MissingParameterException

def transform_title(title: str) -> str:
    start = title.find('$')
    end = title.rfind('$')
    result = r'' + title[start:end + 1]
    if 'y' in result:
        result = result.replace('y', 'f(x)')
    return result

def check_params(fig, ax, f, X):
    all_defined = all(var is not None for var in (fig, ax, f, X))
    all_undefined = all(var is None for var in (fig, ax, f)) and len(X) == 0
    if not (all_defined or all_undefined):
        missing = list(var for var, val in zip(['figure', 'axis', 'function', 'X_values'], [fig, ax, f, X]) if val is None)
        raise MissingParameterException('Not all parameters entered. Enter all parameters or none at all.\n\t'
                                        f'Missing parameters: {missing}')