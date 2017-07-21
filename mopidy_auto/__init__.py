from __future__ import unicode_literals

import logging
import os

from mopidy import config, ext

import tornado.web

from .web import IndexHandler, VolumeHandler

__version__ = '0.3.0'

logger = logging.getLogger(__name__)


class Extension(ext.Extension):

    dist_name = 'Mopidy-Auto'
    ext_name = 'auto'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema['admin_key'] = config.String()
        schema['cookie_secret'] = config.String()
        schema['base_path'] = config.String()
        schema['max_tracks'] = config.Integer()
        for index in range(3):
            schema["s{}_start".format(index)] = config.String()
            schema["s{}_folder".format(index)] = config.String()
            schema["s{}_max_volume".format(index)] = config.Integer()
        return schema

    def setup(self, registry):
        from .frontend import AutoFrontend
        registry.add('frontend', AutoFrontend)

        registry.add('http:app', {
            'name': self.ext_name,
            'factory': self.webapp
        })

    def webapp(self, config, core):
        return [
            (r'/(index.html)?', IndexHandler, dict(core=core, config=config)),
            (r'/max_volume', VolumeHandler, dict(core=core)),
            (r'/(.*)', tornado.web.StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'static')}),
        ]
