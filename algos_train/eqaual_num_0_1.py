

from typing import List
from collections import defaultdict


def solve(arr: List) -> int:
    """ 0 和 1 个数相等的最长子数组长度. arr: 由0和1组成的数组
    """
    s = 0
    d = {}
    d[0] = -1
    max_len = -1
    for i, e in enumerate(arr):
        if e == 0:
            s += -1
        else:
            s += 1
        if s in d:
            max_len = max(max_len, i - d[s])
        else:
            d[s] = i
    return max_len


arr = [0, 1, 1, 1, 1, 0, 0, 0, 0]
arr = [0, 1] 

ret = solve(arr)
print(ret)
