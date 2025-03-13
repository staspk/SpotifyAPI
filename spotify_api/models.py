from dataclasses import dataclass

@dataclass(frozen=True)
class PlaylistId():
    id:str
    
    def __init__(self, id:str):
        if id is None:
            raise ValueError('Id cannot be None')
        object.__setattr__(self, 'id', id)

    def __str__(self):
        return self.id