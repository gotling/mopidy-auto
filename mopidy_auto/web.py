import os

import tornado.web


class IndexHandler(tornado.web.RequestHandler):
    def initialize(self, core, config):
        self.core = core
        self.config = config
        self.application.settings["cookie_secret"] = self.config['auto']['cookie_secret']

    def get(self, path):
        return self.render('index.html', authed=self.get_secure_cookie('authed', None))

    def post(self, path):
        if self.get_body_argument("password") == '123':
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
