import random, string

class Utils:
    def get_randomized_string(str_length):
        return ''.join(random.choices(string.ascii_letters, k=str_length))
    
    def list_to_str(_list:list[str], char_separator = " "):
        """
        `list_to_str(['a', 'b', 'c'], ';') -> "a;b;c"`
        """
        return char_separator.join(_list)