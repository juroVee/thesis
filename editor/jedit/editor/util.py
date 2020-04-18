from IPython.display import display, HTML


def hide_interactive_toolbars():
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

#.output_wrapper .ui-dialog-titlebar { display: none;}

#<div class="ui-resizable-handle ui-resizable-se ui-icon ui-icon-gripsmall-diagonal-se" style="z-index: 90; display: block;"></div>


def check_parameters(params, logger) -> dict:
    allowed_params = {'figure', 'axes', 'function', 'intervals', 'primes', 'asymptotes', 'config'}
    result = {}
    if len(params) == 0:
        return result
    for param in params.keys():
        if param not in allowed_params:
            logger.write(logger.new_message('Chyba', neznámy_parameter=param, akcia='vykreslenie prednastavenej funkcie'),
                         mini=True)
            return result
    if any(param not in params for param in ['figure', 'axes', 'function', 'intervals']):
        logger.write(
            logger.new_message('Parameters "figure", "axes", "function" and "intervals" are required to analysis your function.\nPlotting default.'),
            mini=True)
        return result
    else:
        others = {k: params[k] for k in set(params) - {'figure', 'axes', 'function'}}
        for param, value in others.items():
            if param == 'X':
                for i, X in enumerate(value):
                    if len(X) < 2:
                        logger.write(logger.new_message(f'Cannot analysis X at position {i}, need at least 2 values.\nPlotting default.'),
                                     mini=True)
                        return result
            if type(value) != list:
                logger.write(logger.new_message('Optional parameters must be in list. E.g. intervals=[X1, ...].\nPlotting default.'),
                             mini=True)
                return result
    return params
