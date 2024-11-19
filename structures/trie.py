class Trie:
    def __init__(self):
        self._root = [0, {}]

    def add(self, key: str) -> bool:
        """Adds a key to the trie"""
        cur = self._root
        res = False
        cnt = 0
        for ch in key:
            cnt += 1
            if ch not in cur[1]:
                cur[1][ch] = [0, {}]
                res = True
            is_last = cnt == len(key)
            if is_last:
                cur[0] += 1
            cur = cur[1][ch]

        return res

    def exists(self, key: str, strict: bool = True) -> bool:
        cur = self._root
        res = False
        for ch in key:
            if ch not in cur[1]:
                return False
            res = cur[0] > 0
            cur = cur[1][ch]
        if strict:
            return res
        return True

    def remove(self, key: str) -> bool:
        cur = self._root
        if not self.exists(key):
            return False
        for cnt, ch in enumerate(key):
            if cnt + 1 == len(key):
                cur[0] -= 1
            if cur[0] == 0 and ch not in cur[1]:
                del cur[1][ch]
            cur = cur[1][ch]
        return True

    def __contains__(self, key: str) -> bool:
        return self.exists(key)
