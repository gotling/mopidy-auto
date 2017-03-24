import random

import datetime

import logging
import pykka

from mopidy import core

logger = logging.getLogger(__name__)


class AutoFrontend(pykka.ThreadingActor, core.CoreListener):
    def __init__(self, config, core):
        super(AutoFrontend, self).__init__()
        self.config = config
        self.core = core

        self.base_path = self.config['auto']['base_path']
        logger.info("Auto base path: %s", self.base_path)
        self.sections = []
        section = 0

        exists = "s{}_folder".format(section) in self.config['auto']
        while exists:
            self.sections.append({
                "hour": self.config['auto']["s{}_hour".format(section)],
                "minute": self.config['auto']["s{}_minute".format(section)],
                "folder": self.config['auto']["s{}_folder".format(section)],
                "max_volume": self.config['auto']["s{}_max_volume".format(section)]
            })
            section += 1
            exists = "s{}_folder".format(section) in self.config['auto']

        if not self.sections:
            logger.error('Could not find any auto sections')
        else:
            logger.info('Found the following auto sections:')
            for section in self.sections:
                logger.info("Start: %02d:%02d Folder: %s, Max Volume: %d%%",
                            section['hour'],
                            section['minute'],
                            section['folder'],
                            section['max_volume']
                )

    def tracklist_changed(self):
        if self.core.tracklist.get_length().get() == 0:
            self.play_random_album()

    def track_playback_ended(self, tl_track, time_position):
        if self.core.tracklist.index(tl_track).get() == self.core.tracklist.get_length().get() - 1:
            self.play_random_album()

    def play_random_album(self):
        section = self.get_section_by_time()
        logger.info("Auto play of random album, folder: %s", section['folder'])
        if self.core.mixer.get_volume().get() > section['max_volume']:
            self.core.mixer.set_volume(section['max_volume'])
        uri = self.base_path + section['folder']
        tracks = self.get_random_album(uri)
        self.play_uris(tracks)

    def get_section_by_time(self):
        now = datetime.datetime.now()

        for section in reversed(self.sections):
            if now.hour >= section['hour'] and now.minute >= section['minute']:
                return section

        return None

    def get_random_album(self, uri):
        track_uris = []
        logger.info("Navigating file structure, URI: %s", uri)

        refs = self.core.library.browse(uri).get()

        for ref in refs:
            if ref.type == 'track':
                track_uris.append(ref.uri)

        if len(track_uris) > 0:
            return track_uris

        rand_idx = random.randint(0, len(refs) - 1)
        return self.get_random_album(refs[rand_idx].uri)

    def play_uris(self, uris):
        logger.info("Found %d tracks", len(uris))

        self.core.tracklist.clear()
        self.core.tracklist.add(uris=uris)
        self.core.playback.play()
