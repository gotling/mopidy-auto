var mopidy = new Mopidy();

/*
** GLOBALS
**/

// For timer
var interval;
var expected;
var trackPosition = 0;
var trackPositionTimer;

/*
** BINDING
**/

// Logging of all events to JS console
mopidy.on(console.log.bind(console));

mopidy.on("state:online", function () {
   // Set buttons depending on state playing or paused/stopped
   mopidy.playback.getState().done(function(state) {
      toggleButtons(state);
   });

   // Update track information
   mopidy.playback.getCurrentTrack().done(function(track) {
      if (track) {
         updateCurrentTrack(track);
      }
   });

    // Update track position
    mopidy.playback.getTimePosition().done(function(timePosition) {
        setTrackPosition(timePosition);
    });

   // Update volume position
   mopidy.playback.getVolume().done(function(volume) {
      setVolumeUi(volume);
   });
});

$('#play').on('click', function() {
   // If tracklist is empty like on startup, trigger clear event to add random album to list
   mopidy.tracklist.getLength().done(function(length) {
      if (length === 0) {
         mopidy.tracklist.clear();
      }
   });
   mopidy.playback.play();

});

$('#pause').on('click', function() {
   mopidy.playback.pause();
});

function fadeToNext(type) {
    var volume;
    toggleButtons('changing');
    mopidy.playback.getVolume().done(function(initialVolume) {
        volume = initialVolume;
        var timer = setInterval(function () {
            volume--;
            mopidy.playback.setVolume(volume);
            if (volume <= 0) {
                clearInterval(timer);
                if (type === 'track') {
                    mopidy.playback.next();
                } else {
                    mopidy.tracklist.clear();
                }

                mopidy.playback.setVolume(initialVolume);
            }
        }, 50);
    });
}

$('#next-track').on('click', function() {
    fadeToNext('track');
});

// By clearing tracklist, a random one will be added and played
$('#next-album').on('click', function() {
   fadeToNext('album');
});

$('#volume').on('change', function() {
   var volume = parseInt($(this).val());
   mopidy.playback.setVolume(volume);
});

/*
** EVENTS
**/

mopidy.on('event:playbackStateChanged', function(event) {
   toggleButtons(event.new_state);
   stopTimeTicker();
});

mopidy.on("event:trackPlaybackStarted", function(event) {
   updateCurrentTrack(event.tl_track.track);
   setTrackPosition(0);
   startTimeTicker(event.time_position)
});

mopidy.on('event:volumeChanged', function(event) {
   setVolumeUi(event.volume);
});

mopidy.on('event:trackPlaybackResumed', function(event) {
   updateCurrentTrack(event.tl_track.track);
   startTimeTicker(event.time_position)
});

mopidy.on('event:seeked', function(event) {
   setTrackPosition(event.time_position);
});

mopidy.on('event:trackPlaybackPaused', function(event) {
   stopTimeTicker();
});

/*
** FUNCTIONS
**/

// Display track info with error handling for empty values
function updateCurrentTrack(track) {
    if (!track.name) {
       track.name = {"name": "Unknown"}
   }
   $('#current-track').text(track.name);

   if (!track.artists) {
       track.artists = [{"name": "Unknown"}];
   }
   $('#current-artist').text(track.artists[0].name);

   if (!track.album) {
       track.album = {"name": "Unknown"}
   }
   $('#current-album').text(track.album.name);

   $('#track-length').text(msToTimeString(track.length));

   document.title = track.name + ' - Mopidy Auto';
}

function setTrackPosition(newPosition) {
    if (newPosition || newPosition === 0) {
        trackPosition = newPosition;
    }
    $('#track-position').text(msToTimeString(trackPosition));
}

function setVolumeUi(volume) {
   $('#volume').val(volume);
}

function toggleButtons(state) {
   if (state === 'playing') {
        $('#play-div').hide();
        $('#pause-div').show();
        $('.next-button').removeClass('disabled');
   } else if (state === 'changing') {
       $('.next-button').addClass('disabled');
   } else {
        $('#play-div').show();
        $('#pause-div').hide();
        $('.next-button').addClass('disabled');
   }
}

// Update track position, check if timer has drifted and adjust accordingly
function updateCurrentTrackPosition() {
    // The drift (positive for overshooting)
    var dt = Date.now() - expected;
    if (dt > interval) {
        // If drifted more than 1 second, get correct value from Mopidy
        mopidy.playback.getTimePosition().done(function(timePosition) {
            trackPosition = timePosition;
        });
    }

    setTrackPosition();

    expected += interval;
    trackPosition += interval;
    // Restart timeout, taking drift into account
    trackPositionTimer = setTimeout(updateCurrentTrackPosition, Math.max(0, interval - dt));
}

function startTimeTicker(startValue) {
    if (startValue) {
        trackPosition = startValue;
    }

    // Call update function every ms
    interval = 1000;
    // Variable to check how much timer is drifting
    expected = Date.now() + interval;

    trackPositionTimer = setTimeout(updateCurrentTrackPosition, interval);
}

function stopTimeTicker() {
    clearTimeout(trackPositionTimer);
}

/*
** HELPERS
**/
function msToTimeString(ms) {
   var seconds = parseInt(ms / 1000);
   var minutes = parseInt(seconds / 60);
   seconds = seconds % 60;
   return minutes + ":" + pad(seconds, 2);
}

function pad(n, width, z) {
   z = z || '0';
   n = n + '';
   return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
}