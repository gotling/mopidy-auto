import logging
import os
import shutil
import urllib
import urlparse

import tornado.web

logger = logging.getLogger(__name__)


class IndexHandler(tornado.web.RequestHandler):
    def initialize(self, core, config):
        self.core = core
        self.config = config
        self.application.settings["cookie_secret"] = self.config['auto']['cookie_secret']

    def get(self, path):
        return self.render('index.html', authed=self.get_secure_cookie('authed', None))

    def post(self, path):
        action = self.get_body_argument("action", False)
        if action:
            track = self.core.playback.get_current_track().get()
            if track:
                track_path = urllib.url2pathname(urlparse.urlparse(track.uri.split('file://')[1]).path)
                if action == 'delete-track':
                    self.core.playback.next()
                    try:
                        os.remove(track_path)
                        logger.info("Deleted track '{}'".format(track.name))
                    except OSError:
                        logger.error("Could not delete track '{}'".format(track.name), exc_info=1)
                elif action == 'delete-album':
                    album_path = os.path.dirname(track_path)
                    self.core.tracklist.clear()
                    try:
                        shutil.rmtree(album_path, True)
                        logger.info("Deleted album '{}'".format(track.album.name))
                    except shutil.Error:
                        logger.error("Could not delete album '{}'".format(track.album.name), exc_info=1)
                elif action == 'move-album':
                    print('Move current album')
                    return self.redirect('/move')
        elif self.get_body_argument('lock', False):
            self.clear_cookie('authed')
            return self.render('index.html', authed=False)
        elif self.get_body_argument("password") == self.config['auto']['admin_key']:
            self.set_secure_cookie('authed', 'true')
            return self.render('index.html', authed=True)

        return self.get(path)

    def get_template_path(self):
        return os.path.join(os.path.dirname(__file__), 'static')


class MoveHandler(tornado.web.RequestHandler):
    def initialize(self, core, config):
        self.core = core
        self.config = config

        # Store path of currently playing album
        track = self.core.playback.get_current_track().get()
        if track:
            track_path = urllib.url2pathname(urlparse.urlparse(track.uri.split('file://')[1]).path)
            self.album_path = os.path.dirname(track_path)
        else:
            return self.redirect('/auto')

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

    def get(self):
        return self.render('static/move.html', sections=self.sections, current=self.album_path)

    def post(self):
        to = self.get_body_argument("to", False)

        if to:
            destination_uri = os.path.join(self.config['auto']['base_path'], to)
            destination_path = urllib.url2pathname(urlparse.urlparse(destination_uri.split('file://')[1]).path)

            logger.info("Moving '{}' to '{}'".format(self.album_path, destination_path))

            self.core.tracklist.clear()
            try:
                shutil.move(self.album_path, destination_path)
                logger.info("Moved album '{}' to '{}'".format(self.album_path, destination_path))
            except shutil.Error:
                logger.error("Could not move album '{}' to '{}'".format(self.album_path, destination_path), exc_info=1)
        else:
            logger.error('Destination not supplied, move canceled')

        return self.redirect('/auto')


class VolumeHandler(tornado.web.RequestHandler):
    def initialize(self, core):
        self.core = core

    def get(self):
        self.write("{}".format(80))
