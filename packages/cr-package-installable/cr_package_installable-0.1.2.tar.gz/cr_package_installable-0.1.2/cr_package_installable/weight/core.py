"""Conversions between ounces and larger imperial weight units"""
OUNCES_PER_POUND = 16.0  # 16 ounces in a pound
OUNCES_PER_STONE = OUNCES_PER_POUND * 14.0  # 14 pounds in a stone

UNITS = ("oz", "lb", "st")


def ounces_to_pounds(x, reverse=False):
    """
    Convert between ounces and pounds.

    This function converts a given value from ounces to pounds or from pounds to ounces,
    depending on the `reverse` flag.

    Parameters
    ----------
    x : float or int
        The value in ounces (or pounds, if `reverse=True`) to be converted.
        
    reverse : bool, optional
        If True, converts pounds to ounces. If False (default), converts ounces to pounds.

    Returns
    -------
    float
        The converted value, either in pounds or ounces depending on the `reverse` flag.
    
    Examples
    --------
    Convert 16 ounces to pounds:
    
    >>> ounces_to_pounds(16)
    1.0
    
    Convert 1 pound to ounces:
    
    >>> ounces_to_pounds(1, reverse=True)
    16.0
    """
    if reverse:
        return x * OUNCES_PER_POUND
    else:
        return x / OUNCES_PER_POUND



def ounces_to_stone(x, reverse=False):
    """Convert weights between ounces and stone.

    Parameters
    ----------
    x : array_like
        Weights in stone.
    reverse : bool, optional
        If this is set to true this function converts from stone to ounces
        instead of the default behaviour of ounces to stone.

    Returns
    -------
    ndarray
        An array of converted weights with the same shape as `x`. If `x` is a
        0-d array, then a scalar is returned.
    """
    if reverse:
        return x * OUNCES_PER_STONE
    else:
        return x / OUNCES_PER_STONE