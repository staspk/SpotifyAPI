from dataclasses import dataclass


@dataclass()
class ISong():
    title: str
    artist: str
    album: str
    
    def __hash__(self):
        return hash((self.title, self.artist, self.album))
    
    def __str__(self):
        return f'{self.title}:{self.artist}'