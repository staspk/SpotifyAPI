import os, threading
from definitions import ENV


class Env:
    Vars = {}
    PATH_TO_ENV_FILE = ENV
    loaded = False
    mutex = threading.Lock()

    def Load(keys_to_delete = []):
        Env.Vars = {}
        if os.path.exists(Env.PATH_TO_ENV_FILE):
            with open(Env.PATH_TO_ENV_FILE, 'r') as file:
                for line in file:
                    if '=' in line:                                     # Each line must have a "=", truthy (string) key,value, to be written into the record
                        key, value = (line.strip()).split('=', 1)       
                        if key and key not in keys_to_delete:
                            Env.Vars[key] = value
        Env.overwrite()
        Env.loaded = True

    def Save(data:dict|str, value:str=None):
        """ Supports saving either a single `key`/`value`, or saving a `dict` of `data` """
        if Env.loaded is False: Env.Load()
        Env.mutex.acquire()

        if isinstance(data, dict):
            for k, v in data.items():
                if k and v: Env.Vars[k] = v

        elif data and value:
            Env.Vars[data] = value

        Env.overwrite()
        Env.mutex.release()

    def Delete(key:str|list):
        if(isinstance(key, str)): key=[key]
        Env.Load(ENV, keys_to_delete=key)

    def overwrite():
        directory = os.path.dirname(Env.PATH_TO_ENV_FILE)
        if not os.path.exists(directory): os.makedirs(directory, exist_ok=True)
        lines = ""
        for key, value in Env.Vars.items(): lines += f'{key}={value}\n'
        with open(Env.PATH_TO_ENV_FILE, 'w') as file:
            file.write(lines[:-1])
