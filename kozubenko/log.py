import re
from datetime import datetime as dt
from kozubenko.os import Application_Data_Directory, LogFile
from definitions import APP_NAME


errors = LogFile(Application_Data_Directory(APP_NAME), 'errors', dt.now().strftime('%Y-%m-%d'))
server = LogFile(Application_Data_Directory(APP_NAME), 'server', dt.now().strftime('%Y-%m-%d'))

class Log():
    def Error(component:str|None, text:str):
        message = Log.message(component, text)
        errors.prepend(message)

    def Server(text:str):
        message = Log.message('Server', text)
        server.prepend(message)

    def message(component:str|None, text:str):
        if component is None: component = 'None'
        string = f'{dt.now().strftime('%H.%M.%S.%f')}::{component}=>' + '{\n'

        lines = re.split('\r?\n', text)
        for line in lines:
            string += f'  {line}\n'

        string += '}\n'
        return string