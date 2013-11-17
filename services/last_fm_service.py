__author__ = 'zhoutuoyang'
import time
import json
import os
import requests
from models.album import Album
from models.artist import Artist

last_fm_url = 'http://ws.audioscrobbler.com/2.0/'
_MINIMUM_DELAY = 1
TIMEOUT_SEC = 60
delay_time = _MINIMUM_DELAY # default delay after API call in case of banning account
try:
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'last_fm_api_key.txt')) as f:
        api_key = f.read()
except IOError:
    print "There is something wrong with api key file."
    exit()

def get_top_artists(country="UNITED STATES", pages=10):
    """
        Get top artists from a specific country, by default it is United States, using Last.fm API
        Pages argument specifies the front pages of top artists to be fetched, each page contains 50 artists
        If the page argument is over the real limit of page number, the function will stop automatically
        It returns a list of top artists, sorted by popularity, each entry has two properties,
        1. name of artist
        2. mbid, musicbrainz unique ID for the aritist
    """
    artists_container = []
    for page in range(1, pages + 1):
        try:
            response = requests.get(last_fm_url, params={
                'api_key': api_key,
                'method': 'geo.getTopArtists',
                'country': country,
                'format': 'json',
                'page': page
            }, timeout=TIMEOUT_SEC)
        except requests.RequestException as e:
            print e.message
            continue
        if response.status_code == requests.codes.ok:
            top_artists = json.loads(response.text)
            try:
                artists = top_artists['topartists']['artist']
                # type checking
                # last.fm will return an object instead of an array
                # unify the interface here
                if isinstance(artists, dict):
                    artists = [artists]
                attr = top_artists['topartists']['@attr']
                # check whether the current page is the page requested
                # e.g. if there are only 10 pages, when requested the 11th one,
                # Last.fm will still return 10th page
                if int(attr['page']) != page:
                    break
                # put artists in the format needed
                # only name and mbid are necessary
                for artist in artists:
                    artists_container.append(
                        Artist(artist['name'], artist['mbid'])
                    )
            except (KeyError, TypeError) as e:
                print "Encounter improperly formated response"
                print response.text
        delayMe()
    return artists_container


def get_top_albums(artist):
    """
        Get top albums of an object of artist specifiy by the mbid (musicbrainz ID) or arist name,
        otherwise an empty array will return
        The maxium number of albums returned will be less or equal to 10.
    """
    # process arguments
    arguments = {}
    if artist.mbid:
        arguments['mbid'] = artist.mbid
    elif artist.name:
        arguments['artist'] = artist.name
    else:
        return []
    limit = 10
    extra_arguments = {
        'api_key': api_key,
        'method': 'artist.getTopAlbums',
        'format': 'json',
        'limit': limit
    }
    album_container = []
    # request Last.fm
    try:
        response = requests.get(last_fm_url,
                                params=dict(arguments.items() + extra_arguments.items()),
                                timeout=TIMEOUT_SEC)
        if response.status_code == requests.codes.ok:
            top_albums = json.loads(response.text)
            try:
                albums = top_albums['topalbums']['album']
                # type checking
                if isinstance(albums, dict):
                    albums = [albums]
                # generate albums with specific format
                # each entry with name and mbid
                for album in albums:
                    album_container.append(Album(album['name'], album['mbid']))
            except (KeyError, TypeError) as e:
                print "Encounter improperly formated response"
                print response.text
    except requests.RequestException as e:
        print e.message
    delayMe()
    return album_container


def get_album_info(album, artist=None):
    """
        Get album information bsaed on mbid from Last.fm using artist/album or mbid
    """
    # process arguments
    arguments = {}
    if album.mbid:
        arguments['mbid'] = album.mbid
    elif artist and artist.name and album.name:
        arguments['artist'] = artist.name
        arguments['album'] = album.name
    else:
        return {}
    extra_arguments = {
        'api_key': api_key,
        'method': 'album.getInfo',
        'format': 'json',
    }

    # request the album info
    try:
        response = requests.get(last_fm_url,
                                params=dict(arguments.items() + extra_arguments.items()),
                                timeout=TIMEOUT_SEC)
        if response.status_code == requests.codes.ok:
            try:
                # load text into dict
                album_info = json.loads(response.text)['album']
                album.releaseDate = album_info['releasedate']
                ## load the tracks into album
                #album_trimed['tracks'] = [];
            except KeyError as e:
                print "Encounter improperly formated response"
                print response.text
    except requests.RequestException as e:
        print e.message
    delayMe()
    return album


def setDelayTime(time):
    # time must be larger or equal to one sec
    if time >= _MINIMUM_DELAY:
        delay_time = time


def delayMe():
    time.sleep(delay_time)