import os
from definitions import ENV_PATH

class Env:
    vars = {}

    def load(path_to_env_file = ENV_PATH, hard_reset=False):
        if len(Env.vars) == 0:
            with open(path_to_env_file, 'r') as file:
                for line in file:
                    line = line.strip()
                    key, value = line.split('=', 1)
                    Env.vars[key] = value

    def add(key, value):
        Env.vars[key] = value
    
    def get(key):
        return Env.vars.get(key, None)
    
    def save(key, value, path_to_env_file = ENV_PATH):
        with open(path_to_env_file, 'a') as file:
            file.write(f'\n{key}={value}')
        Env.vars[key] = value