from dataclasses import dataclass
from typing import List

@dataclass()
class Song:
    title: str
    artist: str
    album: str
    amount_played: int
    amount_listened: int
    total_ms_played: int
    ts: List[str]

    def __eq__(self, other):
        # if not isinstance(other, Song) or not isinstance(other, LikedSong) or other is None:
        #     raise TypeError
        return self.title == other.title and self.artist == other.artist
    
    def __lt__(self, other):
        return self.total_ms_played < other.total_ms_played
    
    def __hash__(self):
        return hash(self.title, self.artist)
    
    def __repr__(self):
        return f'{self.title}:{self.artist}'
    
    def __str__(self):
        string = ''
        string += f'{self.title} - {self.artist}\n'
        string += f'{self.amount_listened}:{self.amount_played};  '

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

@dataclass
class LikedSong:
    title: str
    artist: str

    def __eq__(self, other):
        return self.title == other.title and self.artist == other.artist 

    def __repr__(self):
        return f'{self.title}:{self.artist}'

    def __str__(self):
        return f'{self.title} - {self.artist}'
