import wx
from wx.lib.gestures import MouseGestures
import Image
import cStringIO

from gui.plugintypes import ListboxPlugin
from gui import pluginutils as utils
from api import API
from sources import covers

# must be named panel
class Panel(ListboxPlugin):
    def __init__(self, parent):
        ListboxPlugin.__init__(self, parent)
        
        self.artcache = covers.cache_covers(API.config.mp3path, [80,80])
        
        # Top level lists as we hit escape
        self.levelorder = (("Albums", API.library.get_album_names),
                           ("Artists", API.library.get_artist_names),
                           ("Songs", API.library.get_song_names),
                           ("Genres", API.library.get_genres),
                           ("Playlists", API.library.get_playlists))

        # start on levelindex + 1 (songs)
        # start on songs because otherwise
        # you'll see horizontal scrollbars
        self.levelindex = 1

        # initially populate with our list
        self.history = []

        # get our items
        self.all = (('All',None,None),)
        title, items = self.get_next_level()
        self.update_titles(title)
        
        # sets up a scrolling list of items
        self.listbox.Bind(wx.EVT_LEFT_UP, self.on_click)
        self.listbox.set_items(items)

        self.Bind(wx.EVT_SET_FOCUS, self.on_focus)

        mg = MouseGestures(self, Auto=False,
                           MouseButton=wx.MOUSE_BTN_LEFT)        
        mg.SetGesturesVisible(True)                        
        mg.AddGesture('D', API.media.change_volume, -0.5)
        mg.AddGesture('U', API.media.change_volume, 0.5)
        mg.AddGesture('R', API.media.next)
        mg.AddGesture('L', API.media.previous)
        #self.attach_gestures(self.content, mg)

        API.media.attach('current', self.check_current)
        
    def on_focus(self, event):
        i = self.listbox.GetFirstSelected()

        if i == -1:
            i = 0

        self.listbox.select(i)
        self.listbox.move(-1)
        self.listbox.move(1)
        
        event.Skip()

    def on_idle(self, event):
        self.set_art()

    def on_click(self, event):
        self.on_enter(self.listbox.GetFirstSelected())
        event.Skip()

    def check_current(self, current):
        for i, item in enumerate(self.listbox.items):
            if current['name'] == item[0]:
                self.listbox.select(i)
                API.log.debug("curr['name']: %s, x[0]: %s", current['name'], item[0])
    
    def handle_key(self, accel, key):
        norm = wx.ACCEL_NORMAL
        shift = wx.ACCEL_SHIFT
        
        if (accel, key) == (norm, wx.WXK_ESCAPE):
            self.on_back()
            
        elif (accel, key) == (norm, wx.WXK_RETURN):
            self.on_enter(self.listbox.GetFirstSelected())

        elif (accel, key) == (norm, wx.WXK_RIGHT):
            self.listbox.move(1)
            
        elif (accel, key) == (norm, wx.WXK_LEFT):
            self.listbox.move(-1)
            
        else:
            raise NotImplementedError

    def update_titles(self, title):
        self.titles = ["","",""]
        for hist in self.history:
            if hist.title:
                self.titles.insert(0,hist.title)

        self.titles.insert(0, title)
        API.log.debug("Titles %s", self.titles)
        self.titles = self.titles[:3]
    
    def on_back(self):
        title = ""
        if self.history:
            hist = self.history.pop()
            if len(self.history) == 1 and len(hist.items) == 1:
                hist = self.history.pop() 
            title = hist.title
            self.listbox.set_items(hist.items, hist.index)
        else:
            title, items = self.get_next_level()
            self.listbox.set_items(items)

        self.update_titles(title)
        
    def get_next_level(self):
        items = None
        while not items:
            self.levelindex = (self.levelindex + 1) % len(self.levelorder)
            try:
                title, func = self.levelorder[self.levelindex]
                items = func()
            except NotImplementedError, e:
                print "skipping", e
                pass

        if self.levelindex != 2:
            items = self.all + items

        return title, items
    
    def on_enter(self, i):
        level_id = self.listbox.GetItemData(i, 1)
        title = self.listbox.GetItemText(i)
        API.log.debug('enter %s %s', i, self.listbox.GetItemData(i, 0))
        self.history.append(HistoryItem(i,level_id,self.listbox.items, self.titles[0]))
        
        # Album top
        if self.levelindex == 0:
            if len(self.history) == 1:
                items = API.library.get_artist_names(album=level_id)
                if len(items) == 1:
                    level_id = items[0][1]
                    self.history.append(HistoryItem(0,level_id,items, None))
                else:
                    items = self.all + items
                    
            if len(self.history) == 2:
                album = self.history[0].level_id
                items = API.library.get_song_names(album=album,artist=level_id)

            if len(self.history) == 3:                
                self.history.pop() # remove from history
                API.media.load_track_and_playlist(i,self.listbox.items,API.media.TYPE_AUDIO)
                return

        # Artist top
        elif self.levelindex == 1:
            if len(self.history) == 1:
                items = API.library.get_album_names(artist=level_id)
                API.log.debug("albums %s", len(items))
                if len(items) == 1:
                    level_id = items[0][1]
                    self.history.append(HistoryItem(0,level_id,items,None))
                else:
                    API.log.debug("adding all")
                    items = self.all + items

            if len(self.history) == 2:
                artist = self.history[0].level_id
                items = API.library.get_song_names(album=level_id,artist=artist)
                API.log.debug("songs %s", len(items))
                
            if len(self.history) == 3:                
                self.history.pop() # remove from history
                API.media.load_track_and_playlist(i,self.listbox.items,API.media.TYPE_AUDIO)
                return

        # Song top
        elif self.levelindex == 2:
            self.history.pop() # remove from history
            API.media.load_track_and_playlist(i,self.listbox.items,API.media.TYPE_AUDIO)
            return

        try:
            self.listbox.set_items(items)
        except UnboundLocalError:
            self.history.pop()
            print "Unknown level"

        self.update_titles(title)

class HistoryItem(object):
    def __init__(self, index, level_id, items, title):
        self.index = index
        self.level_id = level_id
        self.items = items
        self.title = title
