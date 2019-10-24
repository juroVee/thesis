class PlotNotSetException(Exception):
    """Raised when plot data haven't been set"""
    pass

class NotSupportedException(Exception):
    """Raised when % matplotlib notebook is not set"""
    pass