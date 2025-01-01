import os
from definitions import ENV_PATH

class Env:
    loaded = False
    vars = {}

    def load(path_to_env_file = ENV_PATH, key_to_delete:str = None):
        if Env.loaded == False:
            with open(path_to_env_file, 'r') as file:
                for line in file:
                    if '=' in line:                                     # This 4-line-block is responsible for automatically cleaning up on load()
                        key, value = (line.strip()).split('=', 1)       
                        if (key and value) and key != key_to_delete:    #  and also targeted deletion
                            Env.vars[key] = value
            Env._overwrite_dict_to_file(path_to_env_file)
        Env.loaded = True

    def save(key:str, value:str, path_to_env_file = ENV_PATH):
        if Env.loaded == False:
            Env.load(path_to_env_file)

        if key and value:
            Env.vars[key] = value
            Env._overwrite_dict_to_file(path_to_env_file)
        
    def delete(key:str):
        Env.load(ENV_PATH, key_to_delete=key)

    def _overwrite_dict_to_file(path_to_env_file = ENV_PATH):
        with open(path_to_env_file, 'w') as file:
            for key, value in Env.vars.items():
                file.write(f'{key}={value}\n')