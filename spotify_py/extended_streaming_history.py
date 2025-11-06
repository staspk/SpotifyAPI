from dataclasses import dataclass
from kozubenko.print import Print
from kozubenko.json import Json
from .IStreamed import *


@dataclass
class AudioStreamingHistory():
    """
    Analyzes lifetime listening record to find `songs`/`podcasts`/`audiobooks`, sorted by `total_ms_played`. Implementation details: `IStreamed.py`.

    **Requires:** at least one `/Spotify User Data/{name}/Spotify Extended Streaming History/Streaming_History_Audio_***.json`
    """
    songs:   list[StreamedSong]
    podcasts: list[Podcast]
    audiobooks: list[AudioBook]

    total_records: int
    unexpected_records: list[Unidentified]

    name: str

    def console_report(self):
        Print.green(f'{self.name}.history => iterated through {self.total_records} records. Unidentified: {len(self.unexpected_records)}')
        Print.green(f'   Songs      : {self.songs.__len__()}')
        Print.green(f'   Podcasts   : {self.podcasts.__len__()}')
        Print.green(f'   AudioBooks : {self.audiobooks.__len__()}')


class ExtendedStreamingHistory():
    """
    **Requires:** `/Spotify User Data/{name}/Spotify Extended Streaming History`   
    
    ***See: `SpotifyUser.py` for import steps.***
    """

    def Parse(name:str, json_files:list[str]) -> AudioStreamingHistory:
        """
        Pass in List of jsons with *`"Streaming_History_Audio"`* in their filename.  
        
        e.g: `Streaming_History_Audio_2018_1.json`
        """
        songs_streamed:      dict[str, StreamedSong] = {}
        podcasts_streamed:   dict[str, Podcast]      = {}
        audiobooks_streamed: dict[str, AudioBook]    = {}
        
        iterations = 0
        unexpected: list[Unidentified] = []

        for json in json_files:
            for record in Json.load(json):
                iterations += 1
                audio = IStreamed.createFromJsonRecord(record)
                representation = repr(audio)

                if isinstance(audio, StreamedSong):
                    fromDict = songs_streamed.pop(representation, None)
                    if fromDict is not None:
                        audio.combine(fromDict)
                    songs_streamed[representation] = audio

                elif isinstance(audio, Podcast):
                    fromDict = podcasts_streamed.pop(representation, None)
                    if fromDict is not None:
                        audio = audio.combine(fromDict)
                    podcasts_streamed[representation] = audio

                elif isinstance(audio, AudioBook):
                    fromDict = audiobooks_streamed.pop(representation, None)
                    if fromDict is not None:
                        audio = audio.combine(fromDict)
                    audiobooks_streamed[representation] = audio

                elif isinstance(audio, Unidentified):
                    audio.file = json
                    audio.read_cycle = iterations
                    unexpected.append(audio)

        return AudioStreamingHistory(
            sorted(songs_streamed.values()), sorted(podcasts_streamed.values()), sorted(audiobooks_streamed.values()),
            iterations,
            unexpected,
            name
        )
