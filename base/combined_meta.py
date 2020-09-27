from .atom_meta import FinalMeta, NoInstanceMeta


class FinalNoInstanceMeta(FinalMeta, NoInstanceMeta):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs, **kwargs)
