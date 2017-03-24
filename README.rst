****************************
Mopidy-Auto
****************************

.. image:: https://img.shields.io/pypi/v/Mopidy-Auto.svg?style=flat
    :target: https://pypi.python.org/pypi/Mopidy-Auto/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/travis/gotling/mopidy-auto/master.svg?style=flat
    :target: https://travis-ci.org/gotling/mopidy-auto
    :alt: Travis CI build status

.. image:: https://img.shields.io/coveralls/gotling/mopidy-auto/master.svg?style=flat
   :target: https://coveralls.io/r/gotling/mopidy-auto
   :alt: Test coverage

Mopidy plugin to automate music playback


Installation
============

    ! NOT YET

Install by running::

    pip install Mopidy-Auto

Or, if available, install the Debian/Ubuntu package from `apt.mopidy.com
<http://apt.mopidy.com/>`_.


Configuration
=============

Before starting Mopidy, you must add configuration for
Mopidy-Auto to your Mopidy configuration file::

    [auto]
    enabled = true

    # URI where the sections folders are located
    base_path = file:///Users/marcus/Media/Music/

    # Max number of tracks that can be added from one folder. Set to 0 or lower to disable limit
    max_tracks = 15

    # Sections of different music activated depending on time of day. Currently locked to 3
    # At what time this section gets active
    s0_hour = 0
    s0_minute = 0
    # Folder name in where to find albums
    s0_folder = Rap
    # Decrease volume to this level if it is set higher when new folder is being played
    s0_max_volume = 50

    s1_hour = 11
    s1_minute = 0
    s1_folder = Trip Hop
    s1_max_volume = 80

    s2_hour = 18
    s2_minute = 30
    s2_folder = Rock
    s2_max_volume = 80

Project resources
=================

- `Source code <https://github.com/gotling/mopidy-auto>`_
- `Issue tracker <https://github.com/gotling/mopidy-auto/issues>`_


Changelog
=========

v0.1.0 (UNRELEASED)
----------------------------------------

- Initial release.
