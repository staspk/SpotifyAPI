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
    def fp(self, mode='w', encoding='UTF-16'): return open(self, mode, encoding=encoding)

    def contents(self, encoding='UTF-16'):
        with open(self, 'r', encoding=encoding) as file:
            return file.read()
        
    def append(self, _str:str, encoding='UTF-16'):
        directory = os.path.dirname(self)
        if not os.path.exists(directory): os.makedirs(directory, exist_ok=True)
        with open(self, 'a', encoding=encoding) as file:
            file.write(_str)

    def save(self, _str:str, encoding='UTF-16'):
        directory = os.path.dirname(self)
        if not os.path.exists(directory): os.makedirs(directory, exist_ok=True)
        with open(self, 'w', encoding=encoding) as file:
            file.write(_str)

    @staticmethod
    def exists(path:str, *paths:str) -> str|None:
        """
        Returns the `path`, or `False`
        """
        file = os.path.join(path, *paths)
        if(os.path.isfile(file)):
            return file
        return None

class LogFile(File):
    def prepend(self, text:str):
        if File.exists(self):
            with open(self, 'r', encoding='utf-8') as file: existing_text = file.read()
        else: existing_text = ""
        with open(self, 'w', encoding='utf-8') as file: file.write(text + existing_text)
        
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
    def files(path:str, str:str=None) -> list[File]:
        """
        Returns a `List` of `Files`(absolute paths) at `path`. filters by `str in filename`, if `str` not `None`

        **Example:**
        >>>  if(files := Directory.files(EXTENDED_STREAMING_HISTORY, 'Streaming_History_Audio')):
        """
        files:list[File] = []
        if(os.path.exists(path)):
            for file in os.listdir(path):
                if (str):
                    if str in file: files.append(File(os.path.join(path, file)))
                else:
                    files.append(File(os.path.join(path, file)))
        return files

def Application_Data_Directory(app_name:str) -> str:
    """
    - **Windows:** *`C:/Users/{user}/AppData/Roaming/{ApplicationName}`*  
    - **Mac/Linux:** *`home/{user}/.{ApplicationName}/`*
    """
    if os.name == 'nt': path = os.path.join(os.getenv("APPDATA"), app_name)
    else:               path = os.path.join(os.path.expanduser("~"), f'.{app_name}')
    os.makedirs(path, exist_ok=True)
    return path


def Downloads_Directory() -> str:
    r"""
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
