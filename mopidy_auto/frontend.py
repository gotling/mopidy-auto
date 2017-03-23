import random

import datetime
import pykka

from mopidy import core

base_path = 'file:///Users/marcus/Media/Music/'

"""
current_time

for time in times:
    if current_time > start_time and current_time < end_time:
        section = folder



start_time
end_time
folder
max_volume
"""

sections = [
    {"hour": 0, "minute": 0, "folder": "Rap", "max_volume": 80},
    {"hour": 11, "minute": 0, "folder": "Trip Hop", "max_volume": 100},
    {"hour": 19, "minute": 5, "folder": "Rock", "max_volume": 100}
]


class AutoFrontend(pykka.ThreadingActor, core.CoreListener):
    def __init__(self, config, core):
        super(AutoFrontend, self).__init__()
        self.config = config
        self.core = core

    def tracklist_changed(self):
        if self.core.tracklist.get_length().get() == 0:
            self.play_random_album()

    def track_playback_ended(self, tl_track, time_position):
        if self.core.tracklist.index(tl_track).get() == self.core.tracklist.get_length().get() - 1:
            self.play_random_album()

    def play_random_album(self):
        print("Play random album")
        section = self.get_section_by_time()
        print(section)
        uri = base_path + section['folder']
        tracks = self.get_random_album(uri)
        self.play_uris(tracks)

    def get_section_by_time(self):
        now = datetime.datetime.now()

        for section in reversed(sections):
            if now.hour >= section['hour'] and now.minute >=  section['minute']:
                return section

        return None

    def get_random_album(self, uri):
        track_uris = []
        print(uri)

        refs = self.core.library.browse(uri).get()

        for ref in refs:
            if ref.type == 'track':
                track_uris.append(ref.uri)

        if len(track_uris) > 0:
            return track_uris

        rand_idx = random.randint(0, len(refs) - 1)
        return self.get_random_album(refs[rand_idx].uri)

    def play_uris(self, uris):
        print("\n----\nFound {} tracks\n----\n".format(len(uris)))

        self.core.tracklist.clear()
        self.core.tracklist.add(uris=uris)
        self.core.playback.play()
