import os


class Path(str):
    """
    Allows one to use `Path` constructor instead of `os.path.join`. Is a `str`, at it's core.

    **Example:**
        >>>  Path(SPOTIFY_USER_DATA_DIR, self.name, 'Spotify Extended Streaming History')
    """
    def __new__(cls, path, *paths:str):
        return super(Path, cls).__new__(cls, os.path.join(path, *paths))

class File(Path):
    """
    inherits `Path` -> allows you to use `File()` constructor instead of `os.path.join`. Is a `str`, at it's core.
    """
    @staticmethod
    def exists(path:str, *paths:str) -> str|None:
        """
        Returns the `path`, or `False`
        """
        file = os.path.join(path, *paths)
        if(os.path.isfile(file)):
            return file
        return None
    
class Directory(Path):
    """
    inherits `Path` -> allows you to use `Directory()` constructor instead of `os.path.join`. Is a `str`, at it's core.
    """
    @staticmethod
    def exists(path:str, *paths:str) -> str|None:
        """
        Returns the `path`, or `False`
        """
        dir = os.path.join(path, *paths)
        if(os.path.isdir(dir)):
            return dir
        return None
    
    @staticmethod
    def files(path:str, str:str) -> list[str]:
        """
        Returns a `List` of absolute paths of files at `path` with `str in filename`

        **Example:**
        >>>  if(files := Directory.files(EXTENDED_STREAMING_HISTORY, 'Streaming_History_Audio')):
        """
        files:list[File] = []
        if(os.path.exists(path)):
            for file in os.listdir(path):
                if str in file:
                    files.append(File(os.path.join(path, file)))
        return files

def Downloads_Directory() -> str:
    """
    - **Windows:** returns downloads value under: `Registry:SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders`
    - **Mac/Linux:** returns `~/Downloads`
    """
    if os.name == 'nt':
        import winreg
        key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key) as key:
            Downloads_Directory = winreg.QueryValueEx(key, downloads_guid)[0]
            return Downloads_Directory
        
    elif os.name == 'posix':  # Both Mac and Linux
        return os.path.join(os.path.expanduser("~"), "Downloads")