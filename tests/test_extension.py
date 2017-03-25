from __future__ import unicode_literals

import unittest

from mopidy import core

from mopidy_auto import Extension, frontend as frontend_lib


def test_get_default_config():
    ext = Extension()

    config = ext.get_default_config()

    assert '[auto]' in config
    assert 'enabled = true' in config


def test_get_config_schema():
    ext = Extension()

    schema = ext.get_config_schema()
    assert 'base_path' in schema
    assert 'max_tracks' in schema
    for index in range(3):
        assert "s{}_hour".format(index) in schema
        assert "s{}_minute".format(index) in schema
        assert "s{}_folder".format(index) in schema
        assert "s{}_max_volume".format(index) in schema

# TODO Write more test


#def test_get_album(self):
#    self.core = core.Core.start(
#        config, backends=[get_backend(config)]).proxy()
