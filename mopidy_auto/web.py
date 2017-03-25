import os

import tornado.web


class IndexHandler(tornado.web.RequestHandler):
    def initialize(self, core):
        self.core = core

    def get(self, path):
        return self.render('index.html')

    def get_template_path(self):
        return os.path.join(os.path.dirname(__file__), 'static')


class VolumeHandler(tornado.web.RequestHandler):
    def initialize(self, core):
        self.core = core

    def get(self):
        self.write("{}".format(80))
