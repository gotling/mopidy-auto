var mopidy = new Mopidy();

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
   // Update volume position
   mopidy.playback.getVolume().done(function(volume) {
      setVolumeUi(volume);
   });
});

$('#play').on('click', function() {
   // If tracklist is empty like on startup, trigger clear event to add random album to list
   mopidy.tracklist.getLength().done(function(length) {
      console.log(length);
      if (length === 0) {
         console.log('Track list is empty');
         mopidy.tracklist.clear();
      }
   });
   mopidy.playback.play();

});

$('#pause').on('click', function() {
   mopidy.playback.pause();
});

$('#next-track').on('click', function() {
   mopidy.playback.next();
});

// By clearing tracklist, a random one will be added and played
$('#next-album').on('click', function() {
   mopidy.tracklist.clear();
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
});

mopidy.on("event:trackPlaybackStarted", function(event) {
   updateCurrentTrack(event.tl_track.track);
});

mopidy.on('event:volumeChanged', function(event) {
   setVolumeUi(event.volume);
});

/*
** FUNCTIONS
**/

function updateCurrentTrack(track) {
   $('#current-track').text(track.name);
   $('#current-artist').text(track.artists[0].name);
   $('#current-album').text(track.album.name);
}

function setVolumeUi(volume) {
   $('#volume').val(volume);
}

function toggleButtons(state) {
   if (state === 'playing') {
      $('#play-div').hide();
      $('#pause-div').show();
      $('.next-button').removeClass('disabled');
   } else {
      $('#play-div').show();
      $('#pause-div').hide();
      $('.next-button').addClass('disabled');
   }
}