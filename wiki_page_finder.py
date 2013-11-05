from services import freebase_service

__author__ = 'zhoutuoyang'

import os
import time

data_dir = './data'
wiki_dir = './wiki'

def dirChecking():
    """
        Create reviews folder if it does not exist
    """
    if not os.path.exists(wiki_dir):
        os.mkdir(wiki_dir)


def scanArtistJSON():
    """
        Grab all files end with .json
        So make sure that every json file in data dir is about an artist
    """
    for file in os.listdir(data_dir):
        if file.endswith('.json'):
            yield file


if __name__ == '__main__':
    dirChecking()
    for file in scanArtistJSON():
        # remove .json
        artist = file[:-5]
        url = freebase_service.getArtistWikiLink(artist)
        # sleep for half a second
        time.sleep(0.5)
        if url:
            try:
                with open(os.path.join(wiki_dir, artist + '.txt'), mode='w') as f:
                    f.write(url)
            except IOError as e:
                print e.message



