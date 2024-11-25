"""和为k的连续子数组个数
"""
from typing import List
from collections import defaultdict


def solve(arr: List, k) -> int:
    counts = defaultdict(int)
    ret = 0
    s = 0
    for e in arr:
        s += e
        ret += counts[s - k]
        counts[s] += 1
    return ret
