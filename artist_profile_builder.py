__author__ = 'zhoutuoyang'

import os
import json
import time
import re
import data_folder_reader
from services import freebase_service
from services import metacritic_service

freebase_dir = './freebase'
metacritic_dir = './metacritic'

def dirChecking(dir):
    """
        Create reviews folder if it does not exist
    """
    if not os.path.exists(dir):
        os.mkdir(dir)


def convertName(name):
    """
        Convert the illegal name for freebase
    """
    name = re.sub(r'\$', 's', name)
    return name


def buildFBProfiles():
    dirChecking(freebase_dir)
    try:
        for file in data_folder_reader.scanArtistFiles():
            # get artist object
            artist = data_folder_reader.getArtistContent(file)
            try:
                profile = freebase_service.getArtistProfile(convertName(artist.name))
                with open(os.path.join(freebase_dir, re.sub(r"[/]", " ", artist.name) + '.json'), mode='w') as f:
                    f.write(json.dumps(profile, indent=4))
                print u"Finished {0}'s profile file.".format(artist.name)
            except BaseException as e:
                print e
                print u"!!!NO {0}'s profile file.".format(artist.name)
    except BaseException as e:
        print e


def buildMTProfiles():
    dirChecking(metacritic_dir)
    try:
        for file in data_folder_reader.scanArtistFiles():
            # get artist object
            artist = data_folder_reader.getArtistContent(file)
            try:
                # get url
                url = metacritic_service.getArtistUrl(artist.name)
                # get profile
                profile = metacritic_service.scrapeArtistPage(url)
                # sleep
                time.sleep(0.5)
                # build output file
                name = profile[0]
                albums = profile[1]
                NAME_TAG = 'name'
                ALBUM_TAG = '/music/artist/album'
                RELEASE_DATE_TAG = '/music/album/release_date'
                URL_TAG = 'url'
                output = {}
                output[NAME_TAG] = name
                output[ALBUM_TAG] = [{NAME_TAG:album[0],
                                      RELEASE_DATE_TAG:album[1],
                                      URL_TAG:album[2]} for album in albums]
                with open(os.path.join(metacritic_dir, re.sub(r"[/]", " ", artist.name) + '.json'), mode='w') as f:
                    f.write(json.dumps(output, indent=4))
                print u"Finished {0}'s profile file.".format(artist.name)
            except BaseException as e:
                print e
                print u"!!!NO {0}'s profile file.".format(artist.name)
    except BaseException as e:
        print e


if __name__ == '__main__':
    buildMTProfiles()