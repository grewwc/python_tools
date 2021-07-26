from collections import defaultdict
from .exceptions import OperationNotAllowedException

class UF:
    def __init__(self, *, strict=True):
        self._site_type = None
        self._strict = strict
        # not using weakdict becaues CANNOT delete a key in "self._roots" directly
        self._id = {}
        self._roots = {}

    def union(self, p, q, *others):
        if self._strict:
            self._check_type(p, q)

        if p not in self._id:
            self._roots[p] = {p}
            self._id[p] = p

        if q not in self._id:
            self._roots[q] = {q}
            self._id[q] = q

        p_root = self.find(p)
        q_root = self.find(q)
        if p_root == q_root:
            return
        
        # if tree "p_root" is smaller than the tree "q_root"
        if self._sz(p_root) < self._sz(q_root):
            self._id[p_root] = q_root
            self._roots[q_root] = self._roots[q_root].union(self._roots[p_root])
            del self._roots[p_root]
        else:  # "q_root" >= "p_root"
            self._id[q_root] = p_root
            self._roots[p_root] = self._roots[p_root].union(self._roots[q_root])
            del self._roots[q_root]

        # union other items with 'p'
        for item in others:
            self.union(p, item)

    def connected(self, p, q)->bool:
        return self.find(p) == self.find(q)

    def find(self, p):
        """component identifier for p
        if p doesn't exist, return None
        """
        root = p
        if p not in self._id:
            return None

        while root != self._id[root]:
            root = self._id[root]
        # path compression
        while root != p:
            p_parent = self._id[p]
            self._id[p] = root
            p = p_parent
        return root

    @property
    def count(self)->int:
        """number of components
        """
        return len(self._roots)
        
    @count.setter
    def count(self, value):
        raise OperationNotAllowedException("set count NOT allowed!")

    @property
    def links(self)->dict:
        return self._roots

    @links.setter
    def links(self, value):
        raise OperationNotAllowedException("set links NOT allowed!")

    def remove(self, p, *others):
        """ O(N) 
        """
        p_root = self.find(p)
        if p_root == None:
            return

        del self._id[p]

        if p_root == p:
            if self._sz(p) == 1:
                del self._roots[p]
            else:
                # change roots
                self._roots[p].remove(p)
                next_root = next(iter(self._roots[p]))
                self._roots[next_root] = self._roots[p]
                del self._roots[p]

                # change ids
                for v in self._roots[next_root]:
                    self._id[v] = next_root
        else:
            self._roots[p_root].remove(p)

        # remove other items
        for item in others:
            self.remove(item)

    def _check_type(self, p, q):
        if type(p) != type(q):
            raise TypeError(f'type {type(p)}!= {type(q)} ')

        if self._site_type is None:
            self._site_type = type(p)
        elif self._site_type != type(p):
            raise TypeError(f'type {type(p)} != {self._site_type}')

    def _sz(self, p):
        return len(self._roots[p])
