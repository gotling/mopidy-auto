import pykka

from mopidy import core

base_path = 'file:///Users/marcus/Media/Music/'


class AutoFrontend(pykka.ThreadingActor, core.CoreListener):
    def __init__(self, config, core):
        super(AutoFrontend, self).__init__()
        self.config = config
        self.core = core

    def get_random_album(self):

        tracks = self.get_tracks(base_path + 'Rock')
        print("\n----\nFound {} tracks\n----\n".format(len(tracks)))
        uris = []
        for track in tracks:
            uris.append(track.uri)
            print(track.name)

        self.core.tracklist.clear()
        self.core.tracklist.add(uris=uris)
        self.core.playback.play()

    def track_playback_ended(self, tl_track, time_position):
        if self.core.tracklist.index(tl_track).get() == self.core.tracklist.get_length().get() - 1:
            self.get_random_album()

    def get_tracks(self, uri):
        print(uri)
        results = self.core.library.browse(uri).get()
        for result in results:
            if result.type == 'directory':
                return self.get_tracks(result.uri)

        return results
