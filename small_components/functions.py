def print_binary(fname):
    res = ''
    with open(fname, 'rb') as f:
        data = f.read()
    for i, byte in enumerate(data, 1):
        byte:str = bin(byte)[2:].rjust(8,'0')
        res += byte
        if i % 2 == 1:
            res += '  --  '
        else:
            res += '\n'
        
    print(res)
    
if __name__ == "__main__":
    print_binary('C:/Users/User/Desktop/test')