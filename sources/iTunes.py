from xml.dom import pulldom
import datetime

class Library:
    """iTunes Library class

    Presents simple methods for browsing track data stored in an
    Apple iTunes XML Library file."""

    def __init__(self, filename = None):
        self.current = {}
        self.foundFirst = False
        # FIXME: Catch common errors and respond accordingly? What is the Python convention here?
        self.libFile = filename


    def reset(self):
        """Rewind the parser"""
        self.__findTracks()
        

    def load(self, libPath = []):
        """Parse the iTunes Library"""

        if not self.libFile:
            print "No path specified, guessing..."
            if not self.find(libPath): raise IOError
            
        try:        
            self.events = pulldom.parse( self.libFile )
        except IOError:
            print "Unable to read the iTunes Library"
                        

    def __getNextTag(self, tag):
        """Find and return the next occurrance of a given tag"""
        for (event, node) in self.events:
            if event == "START_ELEMENT" and node.tagName==tag:
                return node
        return False



    def __findTracks(self):
        """Take the parsed DOM tree and find the first track

        This returns True if it has found the "Tracks" key. It
        doesn't actually return the first track - for that, do
            getNextTag('dict')
        This method resets the parser, bewarned."""

        self.events.reset()
        
        for (event, node) in self.events:
            if event == "START_ELEMENT" and node.tagName=="key":
                self.events.expandNode( node )
                if node.hasChildNodes and node.childNodes[0].data == 'Tracks':
                    self.__getNextTag('dict') # This is the collection of ALL tracks. Big, so we skip it.
                    return True

        return False

    def __getAll(self, node):
        """Concatenate the content of multiple child nodes"""
        data = ""
        for child in node.childNodes:
            data += child.data
        return data        


    def __readTrack(self, trackNode):
        from time import strptime
        """Digest a track node and return a dictionary"""
        curKey = ""
        data = {}
        for node in trackNode.childNodes:
            if node.hasChildNodes():
                if node.tagName == "key":
                    curKey = self.__getAll(node)
                else:
                    if node.tagName == "integer":
                        data[curKey] = int( self.__getAll(node) )
                    elif node.tagName == "string":
                        data[curKey] = self.__getAll(node)
                    elif node.tagName == "date":
                        # FIXME: Treating dates as strings.
			#<key>Date Added</key><date>2005-07-10T06:55:54Z</date>
                        temp = self.__getAll(node)
                        temp = temp.split('T')[0]
                        ymd = temp.split('-')
                        ymd = map(int,ymd)
                        data[curKey] = datetime.datetime(*ymd)
                        
        if data.has_key('Track ID'):
            return data
        else:
            return False

    def lastTrack(self):
        return self.current

    def __iter__(self):
        return self

    def next(self):
        track = self.getTrack()
        if track:
            return track
        raise StopIteration

    def getTrack(self):
        """Return the next track's details, or False"""

        if self.foundFirst == False:
            # Find the track section if we haven't already
            self.__findTracks()
            self.foundFirst = True
            self.numTracks = 0
            
        track = self.__getNextTag('dict')
        if track:
            self.events.expandNode(track)
            self.numTracks += 1
            trackInfo = self.__readTrack(track)

            if not trackInfo:
                return {}
            else:
                self.current = trackInfo
                return trackInfo
        else:
            return {}



    def find(self, searchPath = []):
        """Look in the usual places for the Library XML file

        First check the path(s) given, if any, for the default exported
        file name, Library.xml. Then check the current directory for 
        the same filename, and finally, check the default location.

        On Windows, the iTunes library exports to XML as a matter of
        course, even though it apparently uses the binary 
        "iTunes 4 Music Library.itl"
        So we look in the current user's "My Documents/My Music/iTunes/"
        folder for "iTunes 4 Music Library.xml"
        
        On OS X, the location is also fixed. I've added that, but it's
        untested.
        """

        # No joy. Make a list of other places to look.
        import os, sys

        # Try the searchPath first.
        if len(searchPath):
          for item in searchPath:
              if os.path.isfile(item):
                  self.libFile = item
                  return True
        
        if sys.platform.__contains__('darwin'):
          # Add the OS X default location.
          searchPath.append( os.path.join( os.path.expanduser('~'), 'Music', 'iTunes', 'iTunes Music Library.xml') )
        else:
          # Default location for "My Documents" is in the User Profile folder
          searchPath.append( os.path.join( os.environ['USERPROFILE'], 'My Documents', 'My Music', 'iTunes', 'iTunes Music Library.xml') )

          # I'm awkward - I moved mine, and I need the registry to find out where.
          # If we can't access the registry, just skip this step.
          try:
            import win32api, win32con
            regkey = win32api.RegOpenKeyEx( win32con.HKEY_CURRENT_USER, 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Shell Folders', 0, win32con.KEY_READ )
            (value, valtype) = win32api.RegQueryValueEx(regkey, 'My Music')
            if valtype == 1: searchPath.append( os.path.join(value, 'iTunes', 'iTunes Music Library.xml') )
          except:
            pass # Occurit faecam


        for path in searchPath:
            if os.path.isfile(path):
                self.libFile = path
                return True

        # Couldn't find anything
        print "Couldn't find it in the usual places"
        return False


class Album:
    """Album container"""

    def __init__(self):
        """Initialise the data structures"""
        self.tracks = []
        self.title = ""
        self.artist = ""
        self.rating = None
        self.length = None
        

    def __getitem__(self, key): return self.data[key]
    def __setitem__(self, key, value):
        """Update rating data if tracks are added"""
        self.data[key] = value

    def addTrack(self, trackInfo):
        """Add track and update metadata (rating, etc)
        
        Also check that necessary track info has been set, even if
        we have to make it up! Unrated tracks are given the average
        rating (though it doesn't exist in the file format, so don't
        save it back!) because an unrated track is more likely to
        be middlingly good and not yet rated than crappy and still
        in the library. This is psychology rather than user testing,
        so mileage will vary. Must test this!
        """
        trackInfo['Artist'] = trackInfo.has_key('Artist') and trackInfo['Artist'] or ""
        trackInfo['Rating'] = trackInfo.has_key('Rating') and trackInfo['Rating'] or 60
        trackInfo['Play Count'] = trackInfo.has_key('Play Count') and trackInfo['Play Count'] or 0
        trackInfo['Total Time'] = trackInfo.has_key('Total Time') and trackInfo['Total Time'] or 0

        # Take the album name from the first track
        if not self.title:
            self.title = trackInfo['Album']

        # FIXME: This will probably mess up Amazon searches for compilations
        if not self.artist:
            self.artist = trackInfo['Artist']
        elif self.artist <> trackInfo['Artist']:
            # More than one artist in this album
            if self.artist <> "Various Artists":
              self.artist = "Various Artists"
        
        self.tracks.append( trackInfo )


    def genAlbumInfo(self):
        self.__genLength()
        self.__genRating()


    def __genRating(self):
        """Recalculate (and set) the album rating

        Cycle through each track, take its rating and normalise it
        to a range of -40 to +40 (by subtracting 60), then sum all
        track ratings.
        TODO: a better calculation involving play-counts and maybe
        last-played date?
        """
        sumRateTime = 0
        for track in self.tracks:
            sumRateTime += track['Total Time'] * track['Rating']
        
        self.rating = (self.length > 30 * 60 * 1000) and (float(sumRateTime) / float(self.length)) or 0.0
        
        
    def __genLength(self):
        """Get the total time-length of the album"""
        sumTimes = 0
        
        for track in self.tracks:
            sumTimes += track['Total Time']
        
        self.length = sumTimes and sumTimes or 1


if __name__ == "__main__":
    import sys
    numTracks = 0

    try:    
        lib = Library(sys.argv[1])
    except IndexError:
        print "You must specify a location for the Library"
        raise SystemExit

    try:
        lib.load()
    except:
        print "Unable to access the iTunes Library"
        raise SystemExit
    
    trackInfo = lib.getTrack()
    while trackInfo:
        numTracks += 1
        try:
            trackInfo = lib.getTrack()
        except EOFError:
            break;

    print "Found %s tracks" % numTracks    
