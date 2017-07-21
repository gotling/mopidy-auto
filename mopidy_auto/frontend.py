import datetime
import logging
import random
import sys

from mopidy import core

import pykka

logger = logging.getLogger(__name__)


class AutoFrontend(pykka.ThreadingActor, core.CoreListener):
    def __init__(self, config, core):
        super(AutoFrontend, self).__init__()
        self.config = config
        self.core = core

        # One history per section
        self.history = {0: [], 1: [], 2: []}

        # Keep track of the current playing section
        self.section = None

        # Where sections folders are located
        self.base_path = self.config['auto']['base_path']

        # Maximum amount of tracks to add per album
        self.max_tracks = self.config['auto']['max_tracks']
        if self.max_tracks <= 0:
            self.max_tracks = sys.maxsize

        logger.info("Auto base path: %s, max tracks: %d", self.base_path, self.max_tracks)

        # Read all section config to an array. Ready for dynamic amount of sections
        self.sections = []
        section = 0

        exists = "s{}_folder".format(section) in self.config['auto']
        while exists:
            self.sections.append({
                "start": self.config['auto']["s{}_start".format(section)],
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
                logger.info("Start: %s Folder: %s, Max Volume: %d%%",
                            section['start'],
                            section['folder'],
                            section['max_volume'])

    # Mopidy events
    # If tracklist has changed and is empty, play a random album
    def tracklist_changed(self):
        if self.core.tracklist.get_length().get() == 0:
            self.play_random_album()

    # If playback has stopped,
    def track_playback_ended(self, tl_track, time_position):
        # on the last track of the tracklist, play a random album
        if self.core.tracklist.index(tl_track).get() == self.core.tracklist.get_length().get() - 1:
            self.play_random_album()
        # and time is in new section, play random album
        elif self.section != self.get_section_by_time()[1]:
            logger.info("Time has changed to new section, play random album")
            self.play_random_album()

    # When resuming playback, check that time still in correct section, otherwise play new random album
    def track_playback_resumed(self, tl_track, time_position):
        if self.section != self.get_section_by_time()[1]:
            logger.info("Time has changed to new section, play random album")
            self.play_random_album()

    # Functions
    def play_random_album(self):
        section_index, self.section = self.get_section_by_time()
        logger.info("Auto play of random album, folder: %s", self.section['folder'])

        # Decrease volume if it's higher than sections max_volume
        if self.core.mixer.get_volume().get() > self.section['max_volume']:
            self.core.mixer.set_volume(self.section['max_volume'])

        # Find a random album from this sections URI
        uri = self.base_path + self.section['folder']
        tracks = self.get_random_album(uri, section_index)

        # and play it's tracks
        self.play_uris(tracks)

    def get_section_by_time(self):
        now = datetime.datetime.now()
        now_minutes = now.hour * 60 + now.minute

        # Loop through sections in reverse to find the most accurate section
        for section in reversed(self.sections):
            section_start = section['start'].split(':')
            section_minutes = int(section_start[0]) * 60 + int(section_start[1])
            logger.info('Get section by time: {} >= {}? {}'
                        .format(now_minutes, section_minutes, now_minutes >= section_minutes))
            if now_minutes >= section_minutes:
                return self.sections.index(section), section

        return None

    def get_random_album(self, uri, section_index):
        track_uris = []
        logger.info("Navigating file structure, URI: %s", uri)

        # Get all directories or tracks at the current URI
        refs = self.core.library.browse(uri).get()

        # Loop through all refs looking for tracks
        for ref in refs:
            if ref.type == 'track':
                track_uris.append(ref.uri)

                # Limit amount of tracks added
                if len(track_uris) >= self.max_tracks:
                    logger.info("Reached maximum tracks from same folder: %d", self.max_tracks)
                    break

        # If tracks were found, save album to history and return tracks
        if len(track_uris) > 0:
            self.history[section_index].append(uri)
            return track_uris

        # If not, limit refs to unplayed ones
        refs = self.get_unplayed_directories(refs, section_index)

        #  and recursively get a random one
        rand_idx = random.randint(0, len(refs) - 1)
        return self.get_random_album(refs[rand_idx].uri, section_index)

    def play_uris(self, uris):
        logger.info("Found %d tracks", len(uris))

        # Clear tracklist
        self.core.tracklist.clear()

        # Add all tracks by URIs
        self.core.tracklist.add(uris=uris)

        # Start playing
        self.core.playback.play()

    def get_unplayed_directories(self, refs, section_index):
        # Get all directories that are not in this sections history
        unplayed = [x for x in refs if x.uri not in self.history[section_index]]

        # If all albums have been played:
        if len(unplayed) == 0:
            logger.info("Unique albums depleted. Clearing history")

            # Return a list containing all albums except the last one played
            unplayed = [x for x in refs if x.uri != self.history[section_index][-1]]

            # And clear the sections history
            self.history[section_index] = []

        return unplayed
