import random, string

class Utils:
    @staticmethod
    def get_randomized_string(str_length):
        return ''.join(random.choices(string.ascii_letters,
                                        k=str_length))
    

def print_yellow(text, new_line=True):
    print(f'\033[93m{text}\033[0m', end='\n' if new_line else '')

def print_white(text, new_line=True):
    print(f'\033[97m{text}\033[0m', end='\n' if new_line else '')

def print_gray(text, new_line=True):
    print(f'\033[37m{text}\033[0m', end='\n' if new_line else '')

def print_dark_gray(text, new_line=True):
    print(f'\033[90m{text}\033[0m', end='\n' if new_line else '')

def print_cyan(text, new_line=True):
    print(f'\033[96m{text}\033[0m', end='\n' if new_line else '')

def print_blue(text, new_line=True):
    print(f'\033[36m{text}\033[0m', end='\n' if new_line else '')

def print_dark_green(text, new_line=True):
    print(f'\033[32m{text}\033[0m', end='\n' if new_line else '')

def print_green(text, new_line=True):
    print(f'\033[92m{text}\033[0m', end='\n' if new_line else '')

def print_dark_red(text, new_line=True):
    print(f'\033[31m{text}\033[0m', end='\n' if new_line else '')

def print_red(text, new_line=True):
    print(f'\033[91m{text}\033[0m', end='\n' if new_line else '')

def print_dark_yellow(text, new_line=True):
    print(f'\033[33m{text}\033[0m', end='\n' if new_line else '')




    