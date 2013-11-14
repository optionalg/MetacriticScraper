__author__ = 'zhoutuoyang'

import os
import json
import re
import data_folder_reader
from services import freebase_service

freebase_dir = './freebase'

def dirChecking():
    """
        Create reviews folder if it does not exist
    """
    if not os.path.exists(freebase_dir):
        os.mkdir(freebase_dir)


def convertName(name):
    """
        Convert the illegal name for freebase
    """
    name = re.sub(r'\$', 's', name)
    return name

if __name__ == '__main__':
    dirChecking()
    try:
        for file in data_folder_reader.scanArtistFiles():
            # get artist object
            artist = data_folder_reader.getArtistContent(file)
            try:
                profile = freebase_service.getArtistProfile(convertName(artist.name))
                with open(os.path.join(freebase_dir, re.sub(r"[/]", " ", artist.name)  + '.json'), mode='w') as f:
                    f.write(json.dumps(profile, indent=4))
                print u"Finished {0}'s profile file.".format(artist.name)
            except BaseException as e:
                print e
                print u"!!!NO {0}'s profile file.".format(artist.name)
    except BaseException as e:
        print e
