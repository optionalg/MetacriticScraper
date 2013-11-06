__author__ = 'zhoutuoyang'

import os
from models.artist import Artist

data_dir = './data'

def scanArtistFiles():
    """
        Grab all files end with .json
        So make sure that every json file in data dir is about an artist
    """
    if os.path.exists(data_dir):
        for file in os.listdir(data_dir):
            if file.endswith('.json'):
                yield file


def getArtistContent(filename):
    """
        Read json file from data dir, and grab corresponding Artist info
    """
    # checking extension
    if not filename.endswith('.json'):
        raise ValueError('this is not a JSON file')
    filepath = os.path.join(data_dir, filename)
    # checking exisitence
    if not os.path.exists(filepath):
        raise IOError('this file does not exist')
    # read file and load into a dict
    try:
        with open(filepath) as f:
            data = json.loads(f.read())
            artist = Artist(data['name'], data['mbid'])
            artist.topAlbums = data['topAlbums']
        return artist
    except IOError:
        raise