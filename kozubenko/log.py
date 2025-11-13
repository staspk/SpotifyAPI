from datetime import datetime as dt
from kozubenko.os import Application_Data_Directory, LogFile


class Log():
    LOG_FILE = LogFile(Application_Data_Directory('Spotify_Api'), dt.now().strftime('%Y-%m-%d'))

    def log(component, text:str):
        string  = f'{dt.now().strftime('%H.%M.%S.%f')}::{component}=>' + '{\n'
        string += f'{text}\n'
        string += '}\n'
        Log.LOG_FILE.prepend(string)