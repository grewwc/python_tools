class ConvinientMixin:
    def is_empty(self):
        if callable(getattr(self, '__len__', None)):
            return len(self) == 0
        raise NotImplementedError(f'__len__ not found in {self}')

    def contains(self, value):
        if callable(getattr(self, '__contains__', None)):
            return value in self 
        raise NotImplementedError(f'__contains__ not found in {self}')


