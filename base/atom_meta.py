class FinalMeta(type):
    """
    final class 
    """
    def __init__(cls, name, bases, attrs, **kwargs):
        cls.__slots__ = ()
        for base in bases:
            if isinstance(base, FinalMeta):
                raise TypeError('the class {} cannot be inherited'
                                .format(base.__name__))


class NoInstanceMeta(type):
    def __init__(cls, *args, **kwargs):
        pass

    def __call__(cls, *args, **kwargs):
        if (args is not None or kwargs is not None):
            print(f"class {cls} is not instantiable. (ignored)")
        return cls
