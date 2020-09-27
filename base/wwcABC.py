import abc
import numpy as np
from pprint import pprint 

class Helper(abc.ABC):
    @property
    def interfaces(self):
        all_public = [attr for attr in dir(self) if
                      not attr.startswith('_') and attr != 'interfaces']
        res = {'properties': [], 'methods': [], 'members':[]}
        for name in all_public:
            try:
                if isinstance(getattr(type(self), name), property):
                    res['properties'].append(name)
            except AttributeError:
                pass
            if callable(getattr(self, name)):
                res['methods'].append(name)
            else:
                res['members'].append(name)
        res['properties'].append('interfaces')
        pprint(res)
        return res

    def _to_column_vec(self, vec):
        if len(vec.shape) == 1:  # array
            vec = vec.reshape(-1, 1)

        return vec

    def _add_const_x(self, X):
        X = self._to_column_vec(X)
        X = np.c_[np.ones(X.shape[0]), X]
        return X
