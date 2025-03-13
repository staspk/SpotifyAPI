from dataclasses import dataclass

@dataclass(frozen=True)
class PlaylistId():
    Id:str
    
    def __init__(self, Id:str):
        if Id is None:
            raise ValueError('Id cannot be None')
        object.__setattr__(self, 'Id', Id)