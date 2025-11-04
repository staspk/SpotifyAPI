
class Utils:
    
    def list_to_str(_list:list[str], char_separator = " "):
        """
        `list_to_str(['a', 'b', 'c'], ';') -> "a;b;c"`
        """
        return char_separator.join(_list)