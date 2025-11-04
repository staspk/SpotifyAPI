import os, json, string, random
from typing import Any

class Json:
    def load(file:str, encoding='UTF-8'):
        """
        returns `json.load(file)`
        """
        with open(file, 'r', encoding=encoding) as _json:
            return json.load(_json)
    
    def exists(path:str, *paths:str, encoding='UTF-8') -> Any | None:
        """
        Utility method for opening files, loading json data in one line.

        **Example:**
        >>> if(data := Json.exists(SPOTIFY_USER_DATA_DIR, self.name, 'Spotify Account Data', 'Userdata.json')):
                self.account_creation_time = datetime.strptime(data['creationTime'], "%Y-%m-%d")
        """
        file = os.path.join(path, *paths)
        if(os.path.isfile(file)):
            return Json.load(file, encoding)
        return None

class Utils:
    def get_randomized_string(str_length):
        return ''.join(random.choices(string.ascii_letters, k=str_length))
    
    def list_to_str(_list:list[str], char_separator = " "):
        """
        `list_to_str(['a', 'b', 'c'], ';') -> "a;b;c"`
        """
        return char_separator.join(_list)