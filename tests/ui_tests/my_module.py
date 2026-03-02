import pydoc


def add(x, y):
    """
    Params:
      x and b are numbers (int or float)
    Returns:
      the sum of x and y.
    """
    return x + y


pydoc.writedoc('my_module')
