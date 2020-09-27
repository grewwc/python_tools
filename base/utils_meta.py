from .combined_meta import FinalNoInstanceMeta


class ConstMeta(FinalNoInstanceMeta):
    original_dict = None

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs,  **kwargs)
        ConstMeta.original_dict = vars(cls).copy()

    def __setattr__(cls, name, value):
        if name not in vars(cls):
            super().__setattr__(name, value)
        elif value != getattr(cls, name) and value is not None:
            raise TypeError(
                'const "{}" cannot be changed, ({} != {})'
                .format(name, value, getattr(cls, name)))
        elif value is None:
            super().__setattr__(name, value)

    @property
    def all(cls):
        return [c for c in vars(cls) if c not in ConstMeta.original_dict]
