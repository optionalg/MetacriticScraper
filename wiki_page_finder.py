
__author__ = 'zhoutuoyang'

import os
import time
import data_folder_reader
from services import freebase_service

wiki_dir = './wiki'

def dirChecking():
    """
        Create reviews folder if it does not exist
    """
    if not os.path.exists(wiki_dir):
        os.mkdir(wiki_dir)


if __name__ == '__main__':
    dirChecking()
    try:
        for file in data_folder_reader.scanArtistFiles():
            # get artist object
            artist = data_folder_reader.getArtistContent(file)
            # get meta data
            artist_name = artist.name
            # get one of the album to get a better reconciliation
            album = artist.topAlbums[0].name if artist.topAlbums else None
            # get link
            url = freebase_service.getArtistWikiLink(artist_name, album)
            # sleep for half a second
            time.sleep(0.5)
            if url:
                try:
                    with open(os.path.join(wiki_dir, artist_name + '.txt'), mode='w') as f:
                        f.write(url)
                    print u"Finished {0}'s WIKI link file.".format(artist_name)
                except IOError as e:
                    print e.message
            else:
                print u"!!!NO {0}'s WIKI link file.".format(artist_name)
    except BaseException as e:
        print e



