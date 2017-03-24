var mopidy = new Mopidy();

/*
** BINDING
**/

mopidy.on(console.log.bind(console));

mopidy.on("state:online", function () {
   mopidy.playback.getState().done(function(state) {
      toggleButtons(state);
   });
   mopidy.playback.getCurrentTrack().done(function(track) {
      if (track) {
         updateCurrentTrack(track);
      }
   });
   mopidy.playback.getVolume().done(function(volume) {
      setVolumeUi(volume);
   });
});

$('#play').on('click', function() {
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

$('#next').on('click', function() {
   mopidy.playback.next();
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
      $('#play').hide();
      $('#next').removeClass('disabled');
      $('#pause').show();
   } else {
      $('#play').show();
      $('#next').addClass('disabled');
      $('#pause').hide();
   }
}