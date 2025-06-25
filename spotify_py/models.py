from dataclasses import dataclass

@dataclass(frozen=True)
class PlaylistId():

    def __init__(self, id:str):
        if not id:
            raise ValueError('Id cannot be Falsy')
        object.__setattr__(self, 'id', id)

    def __str__(self):
        return self.id