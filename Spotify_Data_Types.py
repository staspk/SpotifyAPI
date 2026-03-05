from enum import StrEnum
from typing import Optional
from kozubenko.os import Directory
from definitions import SPOTIFY_USER_DATA_DIR


def USER_DATA_DIR(name:str, data_type:Optional[Spotify_Data_Type]=None) -> Directory:
    """
    - `data_type` - if passed not a `Spotify_Data_Type`, will throw!
    """
    if data_type and data_type not in Spotify_Data_Type:
        raise Exception(f'USER_DATA_DIR(): type(data_type){type(data_type)}. Should be: Spotify_Data_Type!')

    return Directory(SPOTIFY_USER_DATA_DIR, name, data_type)

class Spotify_Data_Type(StrEnum):
    """
    The name of folder inside: `my_spotify_data.zip`, holding the data.

    Acquire/Use: `my_spotify_data.zip`
    -----------------------------
    1. Download zip(s) at: https://www.spotify.com/us/account/privacy/
    2. `py ./import_Spotify_Data.py {name}` **OR**
    3. call: `Import_Spotify_Data(name, absolute_path_to_zip)`

    Data Details:  https://support.spotify.com/us/article/understanding-your-data/
    """
    ACCOUNT_DATA               = 'Spotify Account Data'
    EXTENDED_STREAMING_HISTORY = 'Spotify Extended Streaming History'
    TECHNICAL_LOG              = 'Spotify Technical Log Information'
