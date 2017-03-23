import random

import pykka

from mopidy import core

base_path = 'file:///Users/marcus/Media/Music/'


class AutoFrontend(pykka.ThreadingActor, core.CoreListener):
    def __init__(self, config, core):
        super(AutoFrontend, self).__init__()
        self.config = config
        self.core = core

    def track_playback_ended(self, tl_track, time_position):
        if self.core.tracklist.index(tl_track).get() == self.core.tracklist.get_length().get() - 1:
            uri = base_path + 'Rock'
            tracks = self.get_random_album(uri)
            self.play_uris(tracks)

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

    """
    def get_tracks(self, uri):
        results = self.core.library.browse(uri).get()
        for result in results:
            if result.type == 'directory':
                return self.get_tracks(result.uri)

        return results
    """
    def play_uris(self, uris):
        print("\n----\nFound {} tracks\n----\n".format(len(uris)))

        self.core.tracklist.clear()
        self.core.tracklist.add(uris=uris)
        self.core.playback.play()
