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
- This extension high-jacks many Mopidy events to control playback so it does not play well with other extensions.

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

By logging in with admin key current playing track or album can be deleted.

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

  # Key required to access admin section
  admin_key = 123

  # URI where the sections folders are located
  base_path = file:///media/Music/

  # Max number of tracks that can be added from one folder. Set to 0 or lower to disable limit
  max_tracks = 15

  # Sections of different music activated depending on time of day. Currently locked to 3
  # At what time this section gets active
  s0_start = 00:00
  # Folder name in where to find albums
  s0_folder = Rap
  # Decrease volume to this level if it is set higher when new folder is being played
  s0_max_volume = 50

  s1_start = 11:00
  s1_folder = Trip Hop
  s1_max_volume = 80

  s2_start = 18:30
  s2_folder = Rock
  s2_max_volume = 80


Recommend File backend configuration
====================================

To make sure playback does not stop due to file types unhandled by Mopidy this exclude works well::

  [file]
  ...
  excluded_file_extensions =
    .nfo
    .ini
    .db
    .rtf
    .jpg
    .jpeg
    .png
    .gif
    .log
    .dat
    .txt
    .sfv
    .pls
    .m3u
    .wma
    .mpc
    .htm
    .html
    .aac
    .m4a
    .sfk
    .url
    .cue
    .pdf
    .m3u8
    .bmp
    .lnk
    .bc!
    .BMP
    .psp
    .ape
    .aif
    .rar

Project resources
=================

- `Source code <https://github.com/gotling/mopidy-auto>`_
- `Issue tracker <https://github.com/gotling/mopidy-auto/issues>`_


Changelog
=========

0.4.0
-----

- Handle empty folders gracefully - `#15 <https://github.com/gotling/mopidy-auto/issues/15>`_
- Added move album - `#12 <https://github.com/gotling/mopidy-auto/issues/12>`_

0.3.0
-----

- Change start time setting from sX_hour + sX_minute to sX_start with format hh:mm
- Change next track and album buttons
- Change volume step to 5%
- Fade out volume when changing track - `#13 <https://github.com/gotling/mopidy-auto/issues/13>`_
- Added admin mode with restricted functions - `#1 <https://github.com/gotling/mopidy-auto/issues/1>`_
- Added delete track - `#2 <https://github.com/gotling/mopidy-auto/issues/2>`_
- Added delete album - `#3 <https://github.com/gotling/mopidy-auto/issues/3>`_

0.2.0
-----

- Display time of current playing track - `#9 <https://github.com/gotling/mopidy-auto/issues/9>`_
- Play album from new section when its time is reached - `#8 <https://github.com/gotling/mopidy-auto/issues/8>`_
- Added skip to next album - `#5 <https://github.com/gotling/mopidy-auto/issues/5>`_
- History is stored per section - `#6 <https://github.com/gotling/mopidy-auto/issues/6>`_


0.1.0
-----

- Initial release.
