from dataclasses import dataclass
from spotify_py.ISong import ISong


@dataclass
class Unidentified():
    """
    A Json record in a `Streaming_History_Audio_***.json` with an unexpected shape.
    """
    record:str             # the json record as a str
    file:str       = None  # absolute path of file where this record was found
    read_cycle:int = None  # aka: parser iterations


@dataclass()
class IStreamed():
    """
    A single record in a `Streaming_History_Audio_***.json`  

    `IStreamed` objects can be combined to form totals over a time domain.
    """
    amount_played   = 1     # amount of records
    amount_listened = 0     # amount of finished listens
    total_ms_played: int    # sum of ms_played from each record 
    ts: list[str]           # list of timestamps of each listen
    uri: str

    @staticmethod
    def createFromJsonRecord(record:dict):
        """ Static Constructor for `IStreamed` """
        if record['master_metadata_track_name'] : return StreamedSong(record)
        if record['episode_name']               : return Podcast(record)
        if record['audiobook_title']            : return AudioBook(record)
        else                                    : return Unidentified(record)

    def combine(self, other):
        if isinstance(other, IStreamed):
            self.amount_played = (self.amount_played + other.amount_played)
            self.amount_listened = (self.amount_listened + other.amount_listened)
            self.total_ms_played = (self.total_ms_played + other.total_ms_played)
            self.ts.extend(other.ts)

        return self
    
    def __lt__(self, other):
        """
        This supports: `sorted(songs_streamed.values())`
        """
        if not isinstance(other, IStreamed):
            raise TypeError('__lt__ only possible between classes that implement IStreamed')
        return self.total_ms_played < other.total_ms_played
        
    def __str__(self):
        # string = f'{self.uri}\n'
        string = f'{self.amount_listened}:{self.amount_played};  '

        if self.total_ms_played < 1000:
            string += f'{self.total_ms_played}ms'
            return string
        
        seconds = self.total_ms_played/1000; minutes = seconds/60; hours = minutes/60
        translatedTimeString = f'{seconds:.0f}s'
        if minutes > 1:
            translatedTimeString += f' => {minutes:.2f}m'
        if hours > 1:
            translatedTimeString += f' => {hours:.2f}hrs'

        return string + translatedTimeString

@dataclass()
class StreamedSong(IStreamed, ISong):
    """
    Possible shape of a record in `Streaming_History_Audio_***.json`.

    `spotify_track_uri` will not be null. example form: `spotify:track:4GnkzqMpGmJIGt8geJetwF`
    """
    def __init__(self, record):
        ISong.__init__(self, title=record['master_metadata_track_name'], artist=record['master_metadata_album_artist_name'], album=record['master_metadata_album_album_name'])
        IStreamed.__init__(self, total_ms_played=record['ms_played'], ts=[record['ts']], uri=record['spotify_track_uri'])
        if record.get('reason_end') == 'trackdone':
            self.amount_listened = 1

    def __eq__(self, other):
        return ISong.__eq__(self, other)
    
    def __hash__(self):
        """
        works alongside `__eq__` to make list comprehensions possible.  
        e.g: this `__hash__()` makes this part work `if song not in self._songs_liked` in `lost_song_candidates()`
        """
        return ISong.__hash__(self)

    def __repr__(self):
        return f'Song:{self.title}:{self.artist}'
       
    def __str__(self):
        # string = f'{self.uri}'
        string = f'{ISong.__str__(self)}\n'
        string += f'{IStreamed.__str__(self)}\n'
        string += f'{self.uri}'
        return string

@dataclass()
class Podcast(IStreamed):
    name: str
    show_name:str

    def __init__(self, record):
        self.name      = record['episode_name']
        self.show_name = record['episode_show_name']

        IStreamed.__init__(self, total_ms_played=record['ms_played'], ts=[record['ts']], uri=record['spotify_episode_uri'])
        if record.get('reason_end') == 'trackdone':
            self.amount_listened = 1
            
    def __eq__(self, other):
        if not isinstance(other, Podcast):
            return False
        return (self.name == other.name and self.show_name == other.show_name)
    
    def __repr__(self):
        return f'Podcast:{self.name}:{self.show_name}'
    
    def __str__(self):
        string = f'{self.name} - {self.show_name}\n'
        string += IStreamed.__str__(self)
        return string

@dataclass
class AudioBook(IStreamed):
    audiobook_title: str
    audiobook_chapter_title: str
    audiobook_uri: str
    audiobook_chapter_uri: str

    def __init__(self, record):
        IStreamed.__init__(self, total_ms_played=record['ms_played'], ts=record['ts'], uri=record['audiobook_uri'])
        if record.get('reason_end') == 'trackdone':
            self.amount_listened = 1

        self.audiobook_title = record['audiobook_title']
        self.audiobook_chapter_title = record['audiobook_chapter_title']
        self.audiobook_uri = record['audiobook_uri']
        self.audiobook_chapter_uri = record['audiobook_chapter_uri']

    def __repr__(self):
        return f'AudioBook:{self.audiobook_title}'