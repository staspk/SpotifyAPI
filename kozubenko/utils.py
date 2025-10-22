import json, string, random

class Json:
    def from_file(file:str, encoding='UTF-8'):
        """
        returns `json.load(file)`
        """
        with open(file, 'r', encoding=encoding) as _json:
            return json.load(_json)

class Utils:
    def get_randomized_string(str_length):
        return ''.join(random.choices(string.ascii_letters, k=str_length))
    
    def list_to_str(_list:list[str], char_separator = " "):
        """
        `list_to_str(['a', 'b', 'c'], ';') -> "a;b;c"`
        """
        return char_separator.join(_list)