__author__ = 'zhoutuoyang'


class Artist(object):
    def __init__(self, name, mbid):
        self.name = name
        self.mbid = mbid
        self.topAlbums = []
