from os import PathLike
from typing import Union, Literal

FileDescriptorOrPath = Union[int, str, bytes, PathLike[str], PathLike[bytes]]

WritableTextMode = Literal[
    'w',    # write
    'a',    # append
    'x',    # exclusive create
    'w+',   # write/read
    'a+',   # append/read
    'x+',   # exclusive create/read
    'wt',   # write (text mode)
    'at',   # append (text mode)
    'xt',   # exclusive create (text mode)
    'wt+',  # write/read (text)
    'at+',  # append/read (text)
    'xt+'   # exclusive create/read (text)
]