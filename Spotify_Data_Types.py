from enum import StrEnum


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