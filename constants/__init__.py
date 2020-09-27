from python_tools.base import ConstMeta


class const(metaclass=ConstMeta):

    @classmethod
    def clear(cls):
        '''
        clear all None value constant
        '''
        to_delete = []
        for name, value in vars(cls).items():
            if (value is None) and (name not in ConstMeta.original_dict):
                to_delete.append(name)

        for name in to_delete:
            print(name)
            delattr(cls, name)
