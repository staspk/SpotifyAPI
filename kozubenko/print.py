import sys
from typing import Callable
from kozubenko.typing import FileDescriptorOrPath, WritableTextMode

def redirect_print_to_file(file:FileDescriptorOrPath, mode:WritableTextMode, print_function:Callable):
    """
    Example Use: `redirect_print_to_file(report, 'w', lambda: print_list(problem_chapters))`
    """
    with open(file, mode, encoding="UTF-8") as file:
        old_stdout = sys.stdout
        sys.stdout = file
        try:
            print_function()
        finally:
            sys.stdout = old_stdout

def print_list(_list:list):
    """
    Recommended for more complex lists (but uses repr instead):
     `import pprint`
     `pprint.pprint(_list)`
    """
    for item in _list:
        print(f'{item}\n')

def print_dict(_dict:dict):
    """
    Recommended for more complex dicts (but uses repr instead):
     `import pprint`
     `pprint.pprint(_dict)`
    """
    for key, value in _dict.items():
        print(f'{key}: {value}\n')
    
def print_yellow(text:str, new_line=True):
    if sys.stdout.isatty():
        print(f"\033[93m{text}\033[0m", end='\n' if new_line else "")
    else:
        print(f"{text}", end="\n" if new_line else "")

def print_white(text:str, new_line=True):
    if sys.stdout.isatty():
        print(f"\033[97m{text}\033[0m", end="\n" if new_line else "")
    else:
        print(f"{text}", end="\n" if new_line else "")

def print_gray(text:str, new_line=True):
    if sys.stdout.isatty():
        print(f"\033[37m{text}\033[0m", end="\n" if new_line else "")
    else:
        print(f"{text}", end="\n" if new_line else "")

def print_dark_gray(text:str, new_line=True):
    if sys.stdout.isatty():
        print(f"\033[90m{text}\033[0m", end="\n" if new_line else "")
    else:
        print(f"{text}", end="\n" if new_line else "")

def print_cyan(text:str, new_line=True):
    if sys.stdout.isatty():
        print(f"\033[96m{text}\033[0m", end="\n" if new_line else "")
    else:
        print(f"{text}", end="\n" if new_line else "")

def print_blue(text:str, new_line=True):
    if sys.stdout.isatty():
        print(f"\033[36m{text}\033[0m", end="\n" if new_line else "")
    else:
        print(f"{text}", end="\n" if new_line else "")

def print_dark_green(text:str, new_line=True):
    if sys.stdout.isatty():
        print(f"\033[32m{text}\033[0m", end="\n" if new_line else "")
    else:
        print(f"{text}", end="\n" if new_line else "")

def print_green(text:str, new_line=True):
    if sys.stdout.isatty():
        print(f"\033[92m{text}\033[0m", end="\n" if new_line else "")
    else:
        print(f"{text}", end="\n" if new_line else "")

def print_dark_red(text:str, new_line=True):
    if sys.stdout.isatty():
        print(f"\033[31m{text}\033[0m", end="\n" if new_line else "")
    else:
        print(f"{text}", end="\n" if new_line else "")

def print_red(text:str, new_line=True):
    if sys.stdout.isatty():
        print(f"\033[91m{text}\033[0m", end="\n" if new_line else "")
    else:
        print(f"{text}", end="\n" if new_line else "")

def print_dark_yellow(text:str, new_line=True):
    if sys.stdout.isatty():
        print(f"\033[33m{text}\033[0m", end="\n" if new_line else "")
    else:
        print(f"{text}", end="\n" if new_line else "")

def print_yellow(text:str, new_line=True):
    if sys.stdout.isatty():
        print(f"\033[93m{text}\033[0m", end="\n" if new_line else "")
    else:
        print(f"{text}", end="\n" if new_line else "")

