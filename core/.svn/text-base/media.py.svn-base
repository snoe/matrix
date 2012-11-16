import cPickle
import os
import random
from logger import log

class Media(object):
    STATE_PLAYING = 'playing'
    STATE_STOPPED = 'stopped'
    STATE_PAUSED = 'paused'

    SHUFFLE_NONE = 'none'
    SHUFFLE_TRACK = 'track'
    SHUFFLE_ALBUM = 'album'

    TYPE_AUDIO = 'audio'
    TYPE_VIDEO = 'video'
                                                                    
    def __init__(self, library):
        self.loading = False
        self.library = library
        self._load_saved_state()

        self.mute_volume = self.volume
        self._current = None
        self._update_current(save=False,get_random=False)

        # auto play, config?
        self.state = self.STATE_PLAYING

    def attach(self, key, func):
        # synch to key
        func(getattr(self,key))
        # add this function to be executed when the
        Media._watchers.setdefault(key, []).append(func)


    def _load_saved_state(self):
        try:
            f = open('data/media.current','rb')
            self.index, self.playlist, self.media_type = cPickle.load(f)
        except (IOError, EOFError):
            self.index = 0
            self.playlist = self.library.get_song_names()
            self.media_type = Media.TYPE_AUDIO

        try:
            f = open('data/media.played','rb')
            self.played = cPickle.load(f)
        except IOError:
            self.played = []            

        try:
            f = open('data/media.volume', 'rb')
            self.volume = cPickle.load(f)
        except IOError:
            self.volume = 0.3
            
        try:
            f = open('data/media.shuffle', 'rb')
            self.shuffle = cPickle.load(f)
        except IOError:
            self.shuffle = Media.SHUFFLE_NONE

    def _update_current(self, save=True, get_random=True):
        if get_random and self.shuffle != Media.SHUFFLE_NONE:
            if self.shuffle == Media.SHUFFLE_TRACK or self.media_type == Media.TYPE_VIDEO:
                log.debug("picking random")
                if len(self.played) == len(self.playlist):
                    self.played = []

                notplayed = [x for x in range(len(self.playlist)) if x not in self.played]
                self.index = random.choice(notplayed)

            elif self._current and self.shuffle == Media.SHUFFLE_ALBUM:
                album = self.current['album']
                artist = self.current['artist']
                trackid = self.current['track_id']

                nextindex = -1

                if album != None and artist != None:
                    albumsongs = self.library.get_song_names(album, artist)
                    for i, (xname, xid, xfile) in enumerate(albumsongs):
                        if xid == trackid:
                            tempindex = i + 1
                            if tempindex < len(albumsongs):
                                try:
                                    nextindex = list(self.playlist).index(albumsongs[tempindex])
                                    log.debug("found next song in album: %s", nextindex)
                                except ValueError:
                                    pass
                            break

                if nextindex == -1:
                    otheralbum = list(set(self.playlist) - set(albumsongs))
                    xname, xid, xfile = random.choice(otheralbum)
                    song = self.library.get_song_struct(xid)
                    albumsongs = self.library.get_song_names(song['album'], song['artist'])
                    self.index = list(self.playlist).index(albumsongs[0])
                    log.debug("skipping to new album: %s", self.index)
                else:
                    self.index = nextindex

        if save:
            # save new state
            f = open('data/media.current','wb')
            cPickle.dump((self.index,self.playlist, self.media_type),f)
            
        if self.media_type == Media.TYPE_AUDIO:
            itemname, trackid, artfile = self.playlist[self.index]
            # copy index into played
            self.played.append(int(self.index))
            self.current = self.library.get_song_struct(trackid)

        if self.media_type == Media.TYPE_VIDEO:
            itemname, location, artfile = self.playlist[self.index]

            # copy index into played
            self.played.append(int(self.index))
            self.current = dict(location = str(location), artist = "", name = itemname)

    def next(self, *args):
        log.debug("next")
        if not self.loading:
            self.index = (self.index + 1) % len(self.playlist)
            self._update_current()
            
    def previous(self, *args):
        log.debug("previous")
        if not self.loading:
            self.index = (self.index - 1) % len(self.playlist)
            self._update_current()

    def play(self, *args):
        self.state = Media.STATE_PLAYING

    def play_pause(self, *args):
        if self.state == Media.STATE_PLAYING:
            self.state = Media.STATE_PAUSED
        else:
            self.state = Media.STATE_PLAYING

    def change_shuffle(self, *args):
        old_shuffle = self.shuffle
        if self.shuffle == Media.SHUFFLE_NONE:
            self.shuffle = Media.SHUFFLE_TRACK
        elif self.shuffle == Media.SHUFFLE_TRACK:
            self.shuffle = Media.SHUFFLE_ALBUM
        elif self.shuffle == Media.SHUFFLE_ALBUM:
            self.shuffle = Media.SHUFFLE_NONE

        if old_shuffle != self.shuffle:
            # save to file
            f = open('data/media.shuffle','wb')
            cPickle.dump(self.shuffle,f)

    def toggle_mute(self, *args):
        if self.volume == 0:
            self.volume = self.mute_volume
        else:
            self.mute_volume = self.volume
            self.volume = 0

    def change_volume(self, amount):
        old_volume = self.volume
        self.volume += amount

        if self.volume > 1:
            self.volume = 1
        if self.volume < 0:
            self.volume = 0
        if self.volume > 0:
            self.mute_volume = self.volume
            
        if old_volume != self.volume:
            log.debug("set_volume %s from %s", amount, self.volume)

            # save to file
            f = open('data/media.volume','wb')
            cPickle.dump(self.volume,f)

    def load_track_and_playlist(self, index, playlist, media_type):
        log.debug("load_track %s %s %s", index, len(playlist), media_type)

        self.index = index
        self.playlist = playlist
        self.media_type = media_type
        self.played = []
        
        self._update_current(get_random=False)

    _watchers = {}
    def run_watchers(key):
        def _deco(f):
            def _inner(self, *args, **kw):
                results = f(self, *args, **kw)
                if key in Media._watchers:
                    for watcher in Media._watchers[key]:
                        watcher(*args, **kw)

                return results
            return _inner
        return _deco

    @run_watchers('state')
    def set_state(self, value):
        self._state = value
    def get_state(self):
        return self._state
    state = property(fget=get_state, fset=set_state)

    @run_watchers('current')
    def set_current(self, value):
        self._current = value
    def get_current(self):
        return self._current
    current = property(fget=get_current, fset=set_current)

    @run_watchers('volume')
    def set_volume(self, value):
        self._volume = value
    def get_volume(self):
        return self._volume
    volume = property(fget=get_volume, fset=set_volume)

    @run_watchers('shuffle')
    def set_shuffle(self, value):
        self._shuffle = value
    def get_shuffle(self):
        return self._shuffle
    shuffle = property(fget=get_shuffle, fset=set_shuffle)

