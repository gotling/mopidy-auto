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

Mopidy extension to automate music playback based on time of day.

Can be used in restaurants to play fitting music depending on time of day with no user input required.

**Notice**

- Only tested with *file://* backend.
- This extension high-jacks many Mopidy events to control playback so does not play well with other extensions.

Consists of a frontend and simple web client.

Frontend
========

If no tracks are playing and a play event is received, or if playback ends, a random album will be added to the
tracklist and playback started.

Album is chosen from one of 3 sections, based on time of day. After an album has been played, it will not play again
until all other albums in it's section has been played.

If volume is set higher than what is configured for the section, it will be lowered before playback starts.

Web Client
==========

The web client is reached on url `/auto/`. It shows which track, artist and album is playing.

It has 3 buttons: **Play / Pause**, skip to **next track** and skip to **next album**.

It also has a volume control.


Installation
============

Install by running::

    pip install Mopidy-Auto

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

0.2.0
-----

- Display time of current playing track - `#9 <../../issues/9>`_
- Play album from new section when its time is reached - `#8 <../../issues/8>`_
- Added skip to next album - `#5 <../../issues/5>`_
- History is stored per section - `#6 <../../issues/6>`_


0.1.0
-----

- Initial release.
