

def singleton(cls):
    """
    singleton decorator
    usage:

    @singleton
    class A(object):
        a = 1
        def __init__(self, x=0):
            self.x = x

    a1 = A(2)
    a2 = A(3)

    """
    _instances = {}

    def wrapper(*args, **kwargs):
        if cls not in _instances:
            _instances[cls] = cls(*args, **kwargs)
        return _instances[cls]

    return wrapper
