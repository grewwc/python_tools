import numpy as np


def __numpy_array_exclude(arr, ith, axis=0):
    slice_list = [slice(None, None, None)] * len(arr.shape)
    slice_list_exclude = [slice(None, None, None)] * len(arr.shape)
    slice_list_include = slice_list_exclude.copy()

    res = None
    last_id = arr.shape[axis] - 1
    res = []

    try:
        begin, end = ith
    except ValueError:
        end = None
        begin, = ith

    if begin < 0:
        begin = 0
    if (end is None) or (end > last_id):
        end = last_id + 1
    if end < 0:
        end = last_id + 1 + end

    if begin == 0:
        slice_list_include[axis] = slice(end, None, None)
        slice_list_exclude[axis] = slice(0, end, None)
        res.append(arr[tuple(slice_list_exclude)])
        res.append(arr[tuple(slice_list_include)])

    elif end == last_id + 1:
        slice_list_exclude[axis] = slice(0, begin, None)
        slice_list_include[axis] = slice(begin, None, None)
        res.append(arr[tuple(slice_list_exclude)])
        res.append(arr[tuple(slice_list_include)])
    else:
        slice_list_front = slice_list.copy()
        slice_list_back = slice_list.copy()
        slice_list_front[axis] = slice(0, begin, None)
        slice_list_back[axis] = slice(end, None, None)
        slice_list_include[axis] = slice(begin, end, None)
        res.append(np.concatenate([arr[tuple(slice_list_front)],
                                   arr[tuple(slice_list_back)]], axis=axis))
        res.append(arr[tuple(slice_list_include)])
    return res


def numpy_array_exclude(arr, ith, axis=0):
    """
    除掉numpy的某一列/行，(可用于多维数组)
    parameters:
        ith: 可以是int，也可以是tuple。 例如：(1,) 或 (1,None) 或 (1,-1)
    return: [array (excluded target), array (included target)]
    """

    if isinstance(ith, (tuple, list)):
        res = __numpy_array_exclude(arr, ith, axis)
    else:  # ith is int
        ith = (ith, ith+1)
        res = __numpy_array_exclude(arr, ith, axis)[0]

    return res


def square_dist_of_two_vec(vec1, vec2):
    return sum(np.sqrt((vec1-vec2)**2))


def loop(arr, k, epochs=1):
    """choose k elements from numpy array "arr"
       repeat for "epochs" times
    """
    n = len(arr)
    count = 0
    i = 0
    while count < epochs:
        if i + k >= n:
            count += 1
            yield np.concatenate([arr[i:n], arr[:k+i-n]])
            i = k + i - n
        else:
            yield arr[i:i+k]
            i += k
