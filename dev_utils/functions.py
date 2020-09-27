def quote_in_quote(line: str, word: str, ix: int):
    if ix == 0:
        return False
    if word == '"""' or word == '"':
        return line[ix-1] == "'" and line[ix+len(word)] == "'"
    else:
        return line[ix-1] == '"' and line[ix+len(word)] == '"'
