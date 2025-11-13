


class labeledStr(str):
    def __new__(cls, value):
        if(not isinstance(value, str)): raise TypeError('labeledStr value must be a str')
        return super(labeledStr, cls).__new__(cls, value)


class String():
    def list(_list:list, flip=False) -> str:
        """ Transforms a list into a pretty string """
        _str = ""
        if(flip):
            _list = reversed(_list)
        for item in _list:
            _str += f'{item}\n\n'
        return _str[:-1]
