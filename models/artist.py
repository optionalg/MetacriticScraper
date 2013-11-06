__author__ = 'zhoutuoyang'

from album import Album


class Artist(object):
    def __init__(self, name, mbid):
        self.name = name
        self.mbid = mbid
        self.topAlbums = []

    def setTopAlbum(self, topAlbums):
        for album in topAlbums:
            self.topAlbums.append(Album(album['name'], album['mbid'], album['releaseDate']))