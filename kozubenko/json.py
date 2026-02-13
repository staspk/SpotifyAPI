import os, json as JSON
from typing import Any
from .os import File

class Json(File):
    """
    inherits `File` -> allows you to use `Json()` constructor instead of `os.path.join`. Is a `str`, at it's core.

    **Example**:
    ```python
        Json(PROJECT_DIR, jsons, 'data.json').save(Response.json())
    ```
    """
    def load(self):
        with open(self, 'r', encoding='UTF-8') as file:
            return JSON.load(file)
        
    def save(self, json:Any):
        """
        - `json` - usually the result of `requests.get(url).json()`
        """
        JSON.dump(json, self.fp(encoding='UTF-8'), indent=2, ensure_ascii=False)

    @staticmethod
    def Load(path:str, encoding='UTF-8'):
        """
        returns data via `json.load(file)`
        """
        with open(path, 'r', encoding='UTF-8') as file:
            return JSON.load(file)

    @staticmethod
    def Exists(path:str, *paths:str, encoding='UTF-8') -> Any | None:
        """
        Utility method for opening files, loading json data in one line.

        **Example:**
        >>> if(data := Json.exists(SPOTIFY_USER_DATA_DIR, self.name, 'Spotify Account Data', 'Userdata.json')):
                self.account_creation_time = datetime.strptime(data['creationTime'], "%Y-%m-%d")
        """
        file = os.path.join(path, *paths)
        if(os.path.isfile(file)):
            return Json.Load(file, encoding)
        return None
    
