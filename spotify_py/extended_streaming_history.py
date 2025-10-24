from __future__ import annotations
from dataclasses import dataclass
from kozubenko.print import print_green
from kozubenko.utils import Json
from .IStreamed import *
# from .IStreamed import IStreamed, StreamedSong, Podcast, AudioBook, Unidentified


@dataclass
class AudioStreamingHistory():
    """
    Analyzes `lifetime listening record` (see: `IStreamed`) to generate lists of `songs`, `podcasts`, `audiobooks`, sorted by `total_ms_played`.  
    """
    songs:   list[StreamedSong]
    podcasts: list[Podcast]
    audiobooks: list[AudioBook]

    total_records: int
    unexpected_records: list[Unidentified]

    @staticmethod
    def From(json_files:list[str]) -> AudioStreamingHistory:
        songs_streamed:      dict[str, StreamedSong] = {}
        podcasts_streamed:   dict[str, Podcast]      = {}
        audiobooks_streamed: dict[str, AudioBook]    = {}
        
        iterations = 0
        unexpected: list[Unidentified] = []

        for json in json_files:
            for record in Json.from_file(json):
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

        return AudioStreamingHistory(songs_streamed, sorted(podcasts_streamed.values()), sorted(audiobooks_streamed.values()), iterations, unexpected)
        return AudioStreamingHistory(sorted(songs_streamed.values()), sorted(podcasts_streamed.values()), sorted(audiobooks_streamed.values()), iterations, unexpected)

    def console_report(self):
        print_green(f'AudioStreamingHistory.From(): iterated through {self.total_records} records. Unidentified: {len(self.unexpected_records)}')
        print_green(f'   Songs      : {self.songs.__len__()}')
        print_green(f'   Podcasts   : {self.podcasts.__len__()}')
        print_green(f'   AudioBooks : {self.audiobooks.__len__()}')

