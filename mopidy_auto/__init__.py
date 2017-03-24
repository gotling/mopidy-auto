from __future__ import unicode_literals

import logging
import os

from mopidy import config, ext


__version__ = '0.1.0'

# TODO: If you need to log, use loggers named after the current Python module
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
        schema['base_path'] = config.String()
        for index in range(3):
            schema["s{}_hour".format(index)] = config.Integer()
            schema["s{}_minute".format(index)] = config.Integer()
            schema["s{}_folder".format(index)] = config.String()
            schema["s{}_max_volume".format(index)] = config.Integer()
        return schema

    def setup(self, registry):
        from .frontend import AutoFrontend
        registry.add('frontend', AutoFrontend)

        # TODO: Edit or remove entirely
        registry.add('http:static', {
            'name': self.ext_name,
            'path': os.path.join(os.path.dirname(__file__), 'static'),
        })
