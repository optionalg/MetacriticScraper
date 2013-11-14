from __builtin__ import file

__author__ = 'zhoutuoyang'

import os
import json
import re
import time
import data_folder_reader
from services import music_album_url

data_dir = './freebase'
reviews_dir = './review'

def dirChecking():
    """
        Create reviews folder if it does not exist
    """
    if not os.path.exists(reviews_dir):
        os.mkdir(reviews_dir)

def searchCandidateReviews(profile):
    """
        Get all candidate reviews from metacrtic.com,
        read them into the a single JSON file in the review dir named after aritst
    """
    # grab name and album info
    NAME = "name"
    ALBUMS = '/music/artist/album'
    RELEASE_TYPE = "/music/album/release_type"
    CONTENT_TYPE = "/music/album/album_content_type"
    # build review file content
    artist_name = profile[NAME]
    albums = profile[ALBUMS]
    # for each album, grab corresponding record
    albums_with_reivews = []
    for album in albums:
        # checking release type
        if album[RELEASE_TYPE] and album[RELEASE_TYPE] == "Single":
            continue
        # checking content type
        if album[CONTENT_TYPE] and album[CONTENT_TYPE][0] != 'Studio album':
            continue
        album['candidates'] = music_album_url.get_candidate_urls(album[NAME])
        albums_with_reivews.append(album)
        # for each call, delay for 1 second
        time.sleep(0.5)
    profile[ALBUMS] = albums_with_reivews
    # build reivew file path
    filepath = os.path.join(reviews_dir, re.sub(r'[/]', ' ', artist_name) + ".json")
    try:
        with open(filepath, 'w') as f:
            f.write(json.dumps(profile, indent=4))
            f.flush()
        print u"Finished {}'s review file".format(artist_name)
    except IOError as e:
        print u"!!! Did not finished {}'s review file".format(artist_name)
        raise e


def scanArtistFiles():
    """
        Grab all files end with .json
        So make sure that every json file in data dir is about an artist
    """
    if os.path.exists(data_dir):
        for file in os.listdir(data_dir):
            if file.endswith('.json'):
                yield file


if __name__ == '__main__':
    dirChecking()
    for file in scanArtistFiles():
        try:
            path = os.path.join(data_dir, file)
            with open(path) as f:
                profile = json.loads(f.read())
                searchCandidateReviews(profile)
        except BaseException as e:
            print e