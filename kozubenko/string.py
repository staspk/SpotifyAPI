


class String():
    def list(list:list) -> str:
        """ Transforms a list into a pretty string """
        _str = ""
        for item in list:
            _str += f'{item}\n\n'
        return _str[:-1]