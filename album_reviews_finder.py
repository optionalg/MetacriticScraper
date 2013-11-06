__author__ = 'zhoutuoyang'

import os
import json
import time
import data_folder_reader
from services import music_album_url, freebase_service

data_dir = './data'
reviews_dir = './review'

def dirChecking():
    """
        Create reviews folder if it does not exist
    """
    if not os.path.exists(reviews_dir):
        os.mkdir(reviews_dir)

def searchCandidateReviews(artist):
    """
        Get all candidate reviews from metacrtic.com,
        read them into the a single JSON file in the review dir named after aritst
    """
    # grab name and album info
    NAME_STR = 'name'
    TOP_ALBUMS = 'topAlbums'
    try:
        artist_name = artist.name
        top_albums = artist.topAlbums
    except KeyError:
        raise KeyError('This artist object is malformed!!!')
    # build review file content
    data = {
        NAME_STR: artist_name,
        TOP_ALBUMS: []
    }
    # for each album, grab corresponding record
    for album in top_albums:
        # checking whether this album is a single album
        # if yes, skip this one
        if freebase_service.checkAlbumSingle(album[NAME_STR], artist_name):
            continue
        album['candidates'] = music_album_url.get_candidate_urls(album[NAME_STR])
        data[TOP_ALBUMS].append(album)
        # for each call, delay for 1 second
        time.sleep(1)
    # build reivew file path
    filepath = os.path.join(reviews_dir, artist_name + ".json")
    try:
        with open(filepath, 'w+') as f:
            f.write(json.dumps(data, indent=4))
            f.flush()
    except IOError as e:
        raise e


if __name__ == '__main__':
    dirChecking()
    try:
        for file in data_folder_reader.scanArtistFiles():
            searchCandidateReviews(data_folder_reader.getArtistContent(file))
    except BaseException as e:
        print e.message