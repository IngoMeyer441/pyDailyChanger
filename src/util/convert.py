

def str2tuple(string, element_type):
    string = string.strip()
    string = string[1:-1]
    elements = string.split(',')
    result = tuple(map(element_type, elements))
    return result