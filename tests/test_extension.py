from __future__ import unicode_literals


from mopidy_auto import Extension


def test_get_default_config():
    ext = Extension()

    config = ext.get_default_config()

    assert '[auto]' in config
    assert 'enabled = true' in config


def test_get_config_schema():
    ext = Extension()

    schema = ext.get_config_schema()
    assert 'admin_key' in schema
    assert 'base_path' in schema
    assert 'max_tracks' in schema
    for index in range(3):
        assert "s{}_start".format(index) in schema
        assert "s{}_folder".format(index) in schema
        assert "s{}_max_volume".format(index) in schema

# TODO Write more test
