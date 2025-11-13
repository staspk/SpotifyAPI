import os, json
from typing import Any

class Json:
    def save(path:str, data:Any, indent=None):
        """
        Code Example:: 
        ```python
        response:requests.Response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data, json=True)
        if response.status_code == 200: Json.save(fr'{OUT}/response.json', response.json)
        ```
        """
        with open(path, 'w') as file:
            if indent: json.dump(data, file, indent=indent)
            else: json.dump(data, file)
            
    def load(file:str, encoding='UTF-8') -> Any | Exception:
        """
        returns data via `json.load(file)`
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
