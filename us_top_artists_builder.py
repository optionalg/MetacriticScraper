from services import last_fm_top_artists

__author__ = 'zhoutuoyang'
import os
import re
import json

"""
    This script will build a huge JSON file for top 500 artists in United Artists.
    The artists are sorted by their popularity
    Each entry comes with corresponding top albums, mbid, name
    Each album comes with title, mbid, release date
"""

data_dir = './data/'


def dataDirCheck():
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)


def writeArtistJSON(artist):
    if not artist.name:
        print "illegal artist object without a name"
        return
    filename = artist.name + '.json'
    # escape file name
    filename = re.sub(r'[/]', ' ', filename)
    try:
        with open(os.path.join(data_dir, filename), 'w+') as f:
            f.write(json.dumps(artist, default=lambda o:o.__dict__, indent=4))
            f.flush()
    except IOError as e:
        print e
        print "failed to write file " + filename


def buildArtistsJSON():
    # get all the artists
    artists = last_fm_top_artists.get_top_artists("UNITED STATES", 10) # by default it is 10 pages, each with 50 aritists
    for artist in artists:
        writeArtistJSON(artist)


# execuation section
if __name__ == '__main__':
    dataDirCheck()
    buildArtistsJSON()