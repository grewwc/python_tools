

class LruCache:
    class Node:
        def __init__(self, key, value, prev=None, next=None) -> None:
            self.key = key
            self.value = value
            self.prev = prev
            self.next = next

        def __repr__(self) -> str:
            return f'{{{self.key}:{self.value}}}'

    def __init__(self, cap: int) -> None:
        self._cap = cap
        self._map = {}
        self._head = LruCache.Node(0, 0)
        self._tail = LruCache.Node(0, 0)
        self._head.next = self._tail
        self._tail = None
        self._count = 0

    def get(self, key):
        node = self._map.get(key, None)
        if node:
            self._move_to_head(node)
            return node.value
        return None

    def put(self, key, value):
        node = self._map.get(key, None)
        if node:
            self._move_to_head(node)
            node.value = value
        else:
            node = LruCache.Node(key, value)
            self._move_to_head(node)
            self._map[key] = node
            self._count += 1
        if self._tail is None:
            self._tail = node

        if self._count > self._cap:
            self._remove_tail()

    def _move_to_head(self, node: "LruCache.Node"):
        prev = node.prev
        next = node.next
        curr_head = self._head.next
        if prev:
            prev.next = next
        if next:
            next.prev = prev
        self._head.next = node
        node.prev = self._head
        node.next = curr_head
        if curr_head:
            curr_head.prev = node

    def _remove_tail(self):
        node = self._tail
        if not node:  # empty cache
            return
        prev = node.prev
        if prev == self._head or not prev:
            return
        prev.next = None
        self._tail = prev
        self._count -= 1
        del self._map[node.key]
        del prev
