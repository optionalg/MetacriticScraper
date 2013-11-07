__author__ = 'zhoutuoyang'

import urllib2
import os
import json
from bs4 import BeautifulSoup

billboard_dir = './billboard'

def getBillBoardTopArtist(year):
    """
        This function get top 100 artists from specific year
    """
    base_url = 'http://www.billboard.com/artists/top-100/{0}?page={1}'
    top100 = []
    for page in range(5):
        cur_url = base_url.format(year, page)
        try:
            soup = BeautifulSoup(urllib2.urlopen(cur_url))
            artists = soup.find_all('article', class_='masonry-brick')
            for artist in artists:
                h1 = artist.find('h1')
                # artists without links have no a tag
                if h1.a:
                    top100.append(h1.a.get_text())
                else:
                    # strip it as well since it has spaces around
                    top100.append(h1.get_text().strip())
        except BaseException:
            raise
    return top100


def getTopArtists(from_year, to_year):
    """
        This methods return a dict with key as year and value as {artist - ranking mapping dict}
    """
    data = {}
    for year in range(from_year, to_year + 1):
        cur_year = {}
        # get an array of top artist from the year
        artists = getBillBoardTopArtist(year)
        # process artist, ranking mapping
        for ranking, artist in enumerate(artists):
            cur_year[artist] = ranking
        data[year] = cur_year
    return data


if __name__ == '__main__':
    if not os.path.exists(billboard_dir):
        os.makedirs(billboard_dir)
    try:
        data = getTopArtists(2000, 2013)
        with open(os.path.join(billboard_dir, "data.json"), 'w') as f:
            f.write(json.dumps(data, indent=4))
        print "Job is finished!!!"
    except BaseException as e:
        print e
