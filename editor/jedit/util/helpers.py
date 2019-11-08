from .custom_errors import MissingParameterException

def transform_title(title: str) -> str:
    start = title.find('$')
    end = title.rfind('$')
    return r'' + title[start:end + 1]

def check_params(fig, ax, X, f):
    all_defined = all(var is not None for var in (fig, ax, X, f))
    all_undefined = all(var is None for var in (fig, ax, X, f))
    if not (all_defined or all_undefined):
        missing = list(var for var, val in zip(['fig', 'ax', 'X', 'f'], [fig, ax, X, f]) if val is None)
        raise MissingParameterException('Not all parameters entered. Enter all parameters or none at all.\n\t'
                                        f'Missing parameters: {missing}')