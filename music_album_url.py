__author__ = 'zhoutuoyang'
import urllib2
import socket
import json
from bs4 import BeautifulSoup

metacritic = "http://www.metacritic.com"
base_url = metacritic + "/search/album/{0}/results"
_TIMEOUT = 60
def get_candidate_urls(album_name):
    result = []
    # replace all spaces with '+' signs
    # remove all '/' signs
    url = base_url.format(album_name.replace(' ', '+').replace('/', ''))
    try:
        soup = BeautifulSoup(urllib2.urlopen(url, timeout=_TIMEOUT))
        albums = soup.find_all('li', class_='result')
        for album in albums:
            releaseDateTag = album.find('span', class_='data')
            titleTag = album.find('h3', class_='product_title').a
            result.append({
                'name': titleTag.get_text().strip(),
                'url': metacritic + titleTag.get('href'),
                'artist': titleTag.get('href').split('/')[-1].replace('-', ' ').title(),
                'releaseDate': releaseDateTag.get_text().strip()
            })
    except (urllib2.URLError, urllib2.HTTPError, socket.timeout) as e:
        print 'Did not get {0} album candidate urls'.format(album_name)
        print e.message
    return result