#!/usr/bin/env python

from lib.path import path
import urlparse
import urllib
from pysqlite2 import dbapi2 as sqlite
import time
import cPickle
import datetime

from logger import log

class Library(object):    
    def __init__(self, mp3path):
        log.debug("Library initializing")
        tracks = []

        # check the date on the xml file,
        # if it is newer than pickle reload
        mypickle = path('data/lib.pickle')
        tracks = None
        itunes = False
        if itunes == True:
            tracks = self.load_itunes()
        else:
            tracks = self.load_folders(mp3path)

        self.conn = sqlite.connect('sqlite', factory=DictConnnection)
        cur = self.conn.cursor()

        columns = set()
        for track in tracks:
            for k,v in track.items():
                k = k.lower()
                k = k.replace(' ','_')
                if v == None:
                    pass
                elif type(v) == int:
                    columns.add(k + " integer")
                elif type(v) == datetime.datetime:
                    columns.add(k + " timestamp")
                else:
                    columns.add(k + "")

        try:
            cur.execute('DROP TABLE song')
        except:
            pass

        sql = u'''
        CREATE TABLE song(
        %s
        )''' % ",\n".join(columns)
        cur.execute(sql)

        for track in tracks:

            parms = []
            parms.append(track.get('Name',None))
            parms.append(track.get('Album',None))
            parms.append(track.get('Artist',None))
            parms.append(track.get('Track Number', 0))
            parms.append(track.get('Track ID', -1))

            location = track.get('Location', None).encode('utf8')

            if itunes:
                url = urlparse.urlparse(location)
                url = urllib.unquote(url[2])
                url = url.replace('C:/', '')
                parms.append(url)
            else:
                parms.append(location)
                
            sql = """
            insert into song
            (name,album,artist,track_number,track_id,location)
            values
            (?, ?, ?, ?, ?, ?)
            """

            try:
                cur.execute(sql, parms)
            except UnicodeEncodeError:
                print 'couldnt store', name, album, artist, type(name)
            except (sqlite.OperationalError, pysqlite2.dbapi2.OperationalError), e:
                print "op error", e, parms
                pass
            except sqlite.IntegrityError, e:
                print "integrityerror", e
                pass

        self.conn.commit()

    def load_folders(self, mp3path):
        import sources.folders
        from datetime import datetime

        saved = path('data/lib.pickle')
        mp3path = path(mp3path)
        log.debug("%s %s", saved, datetime.fromtimestamp(saved.mtime))
        log.debug("%s %s", mp3path, datetime.fromtimestamp(mp3path.mtime))
        if saved.exists and saved.mtime > mp3path.mtime:
            f = open(saved)
            tracks = cPickle.load(f)
        else:
            log.debug("Loading folders")
            tracks = sources.folders.getTracks(mp3path)
            f = open(saved,'wb')
            cPickle.dump(tracks,f)
            log.debug("Done loading %s tracks.", len(tracks))
        return tracks

    def load_itunes(self):
        import sources.iTunes
        libs = []
        libs.append(path('~/My Documents/My Music/iTunes/iTunes Music Library.xml'))
        libs.append(path('~/Music/iTunes/iTunes Music Library.xml'))
        libs.append(path('iTunes Music Library.xml'))
        myxml = ""
        tracks = []
        for filename in libs:
            if filename.expand().exists():
                myxml = filename.expand()
                break
        try:
            if mypickle.mtime < myxml.mtime:
                filepath = str(myxml)
                lib = sources.iTunes.Library(filepath)
                lib.load()
                tracks = list(lib)

                f = open('data/lib.pickle','wb')
                cPickle.dump(tracks,f)
            else:
                f = open('data/lib.pickle')
                tracks = cPickle.load(f)
        except:
            filepath = str(myxml)
            lib = sources.iTunes.Library(filepath)
            lib.load()
            tracks = list(lib)

            f = open('data/lib.pickle','wb')
            cPickle.dump(tracks,f)
        return tracks

    def get_artist_names(self, album=None):
        cur = self.conn.cursor()
        params = []
        wherealbum = ""
        if album:
            wherealbum = "AND album = ?"
            params.append(album)

        sql = """
        SELECT artist, min(location) as location
        FROM song
        WHERE 1=1
        AND artist IS NOT NULL
        %s
        GROUP BY lower(artist)
        ORDER BY lower(artist)
        """ % wherealbum

        cur.execute(sql, params)

        results = cur.fetchall()
        #return label and data
        ret = [(row['artist'], row['artist'], self.get_album_art(row['location'].encode('utf8'))) for row in results]
        return tuple(ret)


    def get_album_names(self, artist=None):
        cur = self.conn.cursor()
        params = []
        whereartist = ""
        if artist:
            whereartist = "AND artist = ?"
            params.append(artist)

        sql = """
        SELECT album, min(location) as location
        FROM song
        WHERE 1=1
        AND album IS NOT NULL
        %s
        GROUP BY album
        ORDER BY lower(album)
        """ % whereartist

        cur.execute(sql, params)

        results = cur.fetchall()
        # return label and data
        ret = [(row['album'], row['album'], self.get_album_art(row['location'].encode('utf8'))) for row in results]
        return tuple(ret)

    def get_genres(self):
        raise NotImplementedError, "Genres"

    def get_playlists(self):
        raise NotImplementedError, "Playlists"

    def get_song_names(self, album=None, artist=None):
        cur = self.conn.cursor()
        params = []
        wherealbum = ""
        whereartist = ""
        order = ""
        if album:
            wherealbum = "AND album=?"
            params.append(album)
        if artist:
            whereartist = "AND artist=?"
            params.append(artist)

        if artist and album and params:
            order = "lower(album), track_number, "

        sql = """
        SELECT name, track_id, location, track_number FROM song
        WHERE 1=1
        AND name is not null
        %s
        %s
        ORDER BY %s lower(name)
        """ % (wherealbum, whereartist, order)
        cur.execute(sql, params)

        results = cur.fetchall()
        ret = []
        for k in results:
            ret.append((k['name'],k['track_id'],self.get_album_art(k['location'].encode('utf8'))))
        return tuple(ret)

    def get_song_struct(self, track_id):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM song WHERE track_id = ?', (track_id,))
        return cur.fetchone()

    def get_album_art(self, loc):
        art = path(loc).parent / 'cover.jpg'
        if art.exists():
            return art
        else:
            return 'plugins/default.png'
        

def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

class DictConnnection(sqlite.Connection):
    def __init__(self, *args, **kwargs):
        sqlite.Connection.__init__(self, *args, **kwargs)

    def cursor(self):
        return DictCursor(self)

class DictCursor(sqlite.Cursor):
    def __init__(self, *args, **kwargs):
        sqlite.Cursor.__init__(self, *args, **kwargs)
        self.row_factory = lambda cur, row: dict_factory(self, row)


if __name__ == '__main__':
    import locale
    control = Control()
    for album in control.getAlbumNames(artist="Tool"):
        print album, album[0]
