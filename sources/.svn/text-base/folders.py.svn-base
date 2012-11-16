#!/usr/bin/env python

from lib.path import path
import tagger

def getTracks(folder):
    p = path(folder)
    tracks = []
    walked = p.walkfiles('*.mp3')
    files = enumerate(walked)
    for i, f in files:
        track = {}
        track['Track ID'] = i
        track['Location'] = unicode(f.abspath(),'utf-8')

        tags = tagger.ID3v2(f)
        for frame in tags.frames:
            vals = frame.strings
            val = None
            if vals and isinstance(vals, list):
                val = vals[0]
                
            if frame.fid == 'TRCK':
                track['Track Number'] = int(val.split('/')[0])
            if frame.fid == 'TALB':
                track['Album'] = val
            if frame.fid == 'TPE1':
                track['Artist'] = val
            if frame.fid == 'TIT2':
                track['Name'] = val
        if 'Name' not in track:
            print "empty tag?", f.abspath()
        else:
            tracks.append(track)
        if 'Location' in track and not track['Location'].endswith('mp3'):
            print repr(track['Location'])

    return tracks
