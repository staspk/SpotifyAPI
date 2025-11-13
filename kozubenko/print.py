import sys, enum
from typing import Callable
from .typing import FileDescriptorOrPath, WritableTextMode


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


def print_dict(_dict:dict):
    """
    Recommended for more complex dicts (but uses repr instead):
     `import pprint`
     `pprint.pprint(_dict)`
    """
    for key, value in _dict.items():
        print(f'{key}: {value}\n')


class ANSI(enum.Enum):
    GREEN       = "\033[92m"
    YELLOW      = "\033[93m"
    RED         = "\033[91m"
    CYAN        = "\033[96m"
    WHITE       = "\033[97m"
    GRAY        = "\033[37m"
    BLUE        = "\033[36m"
    DARK_RED    = "\033[31m"
    DARK_GRAY   = "\033[90m"
    DARK_GREEN  = "\033[32m"
    DARK_YELLOW = "\033[33m"
    RESET       = "\033[0m"

    # 24-bit (TrueColor)
    ROSE_GOLD   = "\033[38;2;255;196;201m"
    LITE_RED   = "\033[38;2;232;107;118m"
    LITE_GREEN = "\033[38;2;96;223;107m"


class Print:
    def list(list:list, color:ANSI=None, flip=False):
        """
        `flip` - i.e: `descending`/`ascending` order
        """
        if(flip):
            list = reversed(list)

        for item in list:
            if(sys.stdout.isatty()):
                print(f'{color.value}{item}{ANSI.RESET.value}\n') if color else print(f'{item}\n')
            else:
                print(f'{item}\n')

    def green(text:str, new_line=True):
        """
        ANSI codes are stripped if `sys.stdout` is not a `terminal`.
        """
        if sys.stdout.isatty():
            print(f"{ANSI.GREEN.value}{text}{ANSI.RESET.value}", end='\n' if new_line else "")
        else:
            print(text, end='\n' if new_line else "")
            
    def yellow(text:str, new_line=True):
        """
        ANSI codes are stripped if `sys.stdout` is not a `terminal`.
        """
        if sys.stdout.isatty():
            print(f"{ANSI.YELLOW.value}{text}{ANSI.RESET.value}", end='\n' if new_line else "")
        else:
            print(text, end='\n' if new_line else "")

    def red(text:str, new_line=True):
        """
        ANSI codes are stripped if `sys.stdout` is not a `terminal`.
        """
        if sys.stdout.isatty():
            print(f"{ANSI.RED.value}{text}{ANSI.RESET.value}", end='\n' if new_line else "")
        else:
            print(text, end='\n' if new_line else "")

    def rose_gold(text:str, new_line=True):
        """
        ANSI codes are stripped if `sys.stdout` is not a `terminal`.
        """
        if sys.stdout.isatty():
            print(f"{ANSI.ROSE_GOLD.value}{text}{ANSI.RESET.value}", end='\n' if new_line else "")
        else:
            print(text, end='\n' if new_line else "")

    def lite_red(text:str, new_line=True):
        """
        ANSI codes are stripped if `sys.stdout` is not a `terminal`.
        """
        if sys.stdout.isatty():
            print(f"{ANSI.LITE_RED.value}{text}{ANSI.RESET.value}", end='\n' if new_line else "")
        else:
            print(text, end='\n' if new_line else "")

    def lite_green(text:str, new_line=True):
        """
        ANSI codes are stripped if `sys.stdout` is not a `terminal`.
        """
        if sys.stdout.isatty():
            print(f"{ANSI.LITE_GREEN.value}{text}{ANSI.RESET.value}", end='\n' if new_line else "")
        else:
            print(text, end='\n' if new_line else "")

    def cyan(text:str, new_line=True):
        """
        ANSI codes are stripped if `sys.stdout` is not a `terminal`.
        """
        if sys.stdout.isatty():
            print(f"{ANSI.CYAN.value}{text}{ANSI.RESET.value}", end='\n' if new_line else "")
        else:
            print(text, end='\n' if new_line else "")

    def white(text:str, new_line=True):
        """
        ANSI codes are stripped if `sys.stdout` is not a `terminal`.
        """
        if sys.stdout.isatty():
            print(f"{ANSI.WHITE.value}{text}{ANSI.RESET.value}", end='\n' if new_line else "")
        else:
            print(text, end='\n' if new_line else "")

    def gray(text:str, new_line=True):
        """
        ANSI codes are stripped if `sys.stdout` is not a `terminal`.
        """
        if sys.stdout.isatty():
            print(f"{ANSI.GRAY.value}{text}{ANSI.RESET.value}", end='\n' if new_line else "")
        else:
            print(text, end='\n' if new_line else "")

    def blue(text:str, new_line=True):
        """
        ANSI codes are stripped if `sys.stdout` is not a `terminal`.
        """
        if sys.stdout.isatty():
            print(f"{ANSI.BLUE.value}{text}{ANSI.RESET.value}", end='\n' if new_line else "")
        else:
            print(text, end='\n' if new_line else "")

    def dark_red(text:str, new_line=True):
        """
        ANSI codes are stripped if `sys.stdout` is not a `terminal`.
        """
        if sys.stdout.isatty():
            print(f"{ANSI.DARK_RED.value}{text}{ANSI.RESET.value}", end='\n' if new_line else "")
        else:
            print(text, end='\n' if new_line else "")

    def dark_gray(text:str, new_line=True):
        """
        ANSI codes are stripped if `sys.stdout` is not a `terminal`.
        """
        if sys.stdout.isatty():
            print(f"{ANSI.DARK_GRAY.value}{text}{ANSI.RESET.value}", end='\n' if new_line else "")
        else:
            print(text, end='\n' if new_line else "")

    def dark_green(text:str, new_line=True):
        """
        ANSI codes are stripped if `sys.stdout` is not a `terminal`.
        """
        if sys.stdout.isatty():
            print(f"{ANSI.DARK_GREEN.value}{text}{ANSI.RESET.value}", end='\n' if new_line else "")
        else:
            print(text, end='\n' if new_line else "")

    def dark_yellow(text:str, new_line=True):
        """
        ANSI codes are stripped if `sys.stdout` is not a `terminal`.
        """
        if sys.stdout.isatty():
            print(f"{ANSI.DARK_YELLOW.value}{text}{ANSI.RESET.value}", end='\n' if new_line else "")
        else:
            print(text, end='\n' if new_line else "")

class Write:
    """
    The no-new-line-at-end version of Print
    """
    def lite_red(text:str):
        """
        ANSI codes are stripped if `sys.stdout` is not a `terminal`.
        """
        if sys.stdout.isatty():
            print(f"{ANSI.LITE_RED.value}{text}{ANSI.RESET.value}", end="")
        else:
            print(text, end="")

    def lite_green(text:str):
        """
        ANSI codes are stripped if `sys.stdout` is not a `terminal`.
        """
        if sys.stdout.isatty():
            print(f"{ANSI.LITE_GREEN.value}{text}{ANSI.RESET.value}", end="")
        else:
            print(text, end="")