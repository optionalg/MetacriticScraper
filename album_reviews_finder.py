__author__ = 'zhoutuoyang'

import os
import json
import time
import music_album_url

data_dir = './data'
reviews_dir = './review'

def dirChecking():
    """
        Create reviews folder if it does not exist
    """
    if not os.path.exists(reviews_dir):
        os.mkdir(reviews_dir)


def scanArtistJSON():
    """
        Grab all files end with .json
        So make sure that every json file in data dir is about an artist
    """
    for file in os.listdir(data_dir):
        if file.endswith('.json'):
            yield file


def getArtistFile(filemame):
    """
        Read json file from data dir, and grab corresponding Artist info
    """
    # checking extension
    if not filemame.endswith('.json'):
        raise ValueError('this is not a JSON file')
    filepath = os.path.join(data_dir, filemame)
    # checking exisitence
    if not  os.path.exists(filepath):
        raise IOError('this file does not exist')
    # read file and load into a dict
    with open(filepath) as f:
        data = json.loads(f.read())
    return data


def searchCandidateReviews(artist):
    """
        Get all candidate reviews from metacrtic.com,
        read them into the a single JSON file in the review dir named after aritst
    """
    # grab name and album info
    NAME_STR = 'name'
    TOP_ALBUMS = 'topAlbums'
    try:
        artist_name = artist[NAME_STR]
        top_albums = artist[TOP_ALBUMS]
    except KeyError:
        raise KeyError('This artist object is malformed!!!')
    # build review file content
    data = {
        NAME_STR: artist_name,
        TOP_ALBUMS: []
    }
    # for each album, grab corresponding record
    for album in top_albums:
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
    for file in scanArtistJSON():
        try:
            searchCandidateReviews(getArtistFile(file))
        except BaseException as e:
            print e.message