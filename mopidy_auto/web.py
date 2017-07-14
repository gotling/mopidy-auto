import os
import shutil
import logging
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
                    os.unlink(track_path)
                    logger.info("Deleted track '{}'".format(track.name))
                elif action == 'delete-album':
                    album_path = os.path.dirname(track_path)
                    self.core.tracklist.clear()
                    shutil.rmtree(album_path, True)
                    logger.info("Deleted album '{}'".format(track.album.name))
                elif action == 'move-album':
                    print('Move current album')
        elif self.get_body_argument("password") == '123':
            self.set_secure_cookie('authed', 'true')
            return self.render('index.html', authed='true')

        return self.get(path)

    def get_template_path(self):
        return os.path.join(os.path.dirname(__file__), 'static')


class VolumeHandler(tornado.web.RequestHandler):
    def initialize(self, core):
        self.core = core

    def get(self):
        self.write("{}".format(80))
