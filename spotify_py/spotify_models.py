from dataclasses import dataclass
from typing import List

@dataclass()
class ISong():
    title: str
    artist: str
    album: str

    def __eq__(self, other):
        if not isinstance(other, ISong):
            return False
        return (self.title == other.title and self.artist == other.artist and self.album == other.album)
    
    def __str__(self):
        return f'{self.title} - {self.artist}'

@dataclass()
class IStreamed:
    amount_played: int
    amount_listened: int
    total_ms_played: int
    ts: List[str]
    uri: str

    @classmethod
    def createFromJsonRecord(cls, record:dict):
        if record['master_metadata_track_name'] is not None:
            return Song(record)
        elif record['episode_name'] is not None:
            return Podcast(record)
        else:
            # print(f'Encountered a null-valued Record in Streaming_History_Audio: timestamp: {record['ts']}')
            return None

    def combine(self, other):
        if isinstance(other, IStreamed):
            self.amount_played = (self.amount_played + other.amount_played)
            self.amount_listened = (self.amount_listened + other.amount_listened)
            self.total_ms_played = (self.total_ms_played + other.total_ms_played)
            self.ts.extend(other.ts)

        return self
    
    def __lt__(self, other):
        if not isinstance(other, IStreamed):
            raise TypeError('__lt__ only possible between classes that implement IStreamed')
        return self.total_ms_played < other.total_ms_played
        
    def __str__(self):
        # string = f'{self.uri}\n'
        string = f'{self.amount_listened}:{self.amount_played};  '

        if self.total_ms_played < 1000:
            string += f'{self.total_ms_played}ms'
            return string
        
        secs = self.total_ms_played/1000; mins = self.total_ms_played/1000/60; hrs = self.total_ms_played/1000/60/60
        translatedTimeString = f'{secs:.0f}s'
        if mins > 1:
            translatedTimeString += f' => {mins:.2f}m'
        if hrs > 1:
            translatedTimeString += f' => {hrs:.2f}hrs'

        return string + translatedTimeString
    

@dataclass()
class Song(ISong, IStreamed):
    def __init__(self, record):
        ISong.__init__(self, title=record['master_metadata_track_name'], artist=record['master_metadata_album_artist_name'], album=record['master_metadata_album_album_name'])
        IStreamed.__init__(self, amount_played=1, amount_listened=0, total_ms_played=record['ms_played'], ts=[record['ts']], uri=record['spotify_track_uri'] )
        if record.get('reason_end') == 'trackdone':
            self.amount_listened = 1

    def __eq__(self, other):
        return ISong.__eq__(self, other)

    def __repr__(self):
        return f'Song:{self.title}:{self.artist}'
       
    def __str__(self):
        # string = f'{self.uri}'
        string = f'{ISong.__str__(self)}\n'
        string += f'{IStreamed.__str__(self)}\n'
        string += f'{self.uri}'
        return string

@dataclass()
class LikedSong(ISong):
    uri:str

    def __repr__(self):
        return f'LikedSong:{self.title}:{self.artist}'

@dataclass()
class Podcast(IStreamed):
    name: str
    show_name:str

    def __init__(self, record):
        self.name = record['episode_name']
        self.show_name=record['episode_show_name']
        IStreamed.__init__(self, amount_played=1, amount_listened=0, total_ms_played=record['ms_played'], ts=[record['ts']], uri=record['spotify_episode_uri'] )
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