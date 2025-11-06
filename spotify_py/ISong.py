from dataclasses import dataclass


@dataclass()
class ISong():
    title: str
    artist: str
    album: str

    def __eq__(self, other):
        if not isinstance(self, ISong):
            return False
        return (self.title == other.title and self.artist == self.artist and self.album == other.album)
    
    def __hash__(self):
        return hash((self.title, self.artist, self.album))
    
    def __str__(self):
        return f'{self.title}:{self.artist}'