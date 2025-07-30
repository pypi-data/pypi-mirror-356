# Define some exceptions
class ShorelineError(Exception):
    """Generic parent exception"""

    pass


class CrsError(ShorelineError):
    """raised if non-projected crs is passed to init"""

    pass


class SlopeError(ShorelineError):
    """raised if there's a problem with the slope"""

    pass


class InputError(ShorelineError):
    """Generic input problems"""

    pass
