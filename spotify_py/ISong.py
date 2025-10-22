from dataclasses import dataclass


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