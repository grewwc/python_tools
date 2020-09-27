def count_start_empty_space(line: str):
    """
    tab == 4 spaces
    """
    res = 0
    for ch in line:
        if ch != ' ' and ch != '\t':
            break
        if ch == '\t':
            res += 4 
        else:
            res += 1

    return res

