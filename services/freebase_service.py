__author__ = 'zhoutuoyang'
import json
import os
import re
import requests

try:
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'google_api_key.txt')) as f:
        api_key = f.read()
except IOError as e:
    print "There is something wrong with api key file."
    exit()

service_url = 'https://www.googleapis.com/freebase/v1/'
rdf_url = service_url + 'rdf'
topic_url = service_url + 'topic'
mqlread_url = service_url + 'mqlread'
reconciliation_url = service_url + 'reconcile'


def reconcile(name, kind, prop=None):
    """
        return mid of matched enitity or first candidate in the array.
        if candidate contains nothing or there is an error or a warning, return empty string
        if requests throws out error, return empty string as well
    """
    # process arguments
    params = {
        'key': api_key
    }
    params['name'] = name
    params['kind'] = kind
    if prop:
        params['prop'] = prop
    params['confidence'] = 0.5

    mid = None
    try:
        response = requests.get(reconciliation_url, params=params)
        result = json.loads(response.text)
        if 'match' in result:
            mid = result['match']['mid']
        elif 'candidate' in result:
            if result['candidate']:
                mid = result['candidate'][0]['mid']
    except requests.RequestException as e:
        print e.message
    return mid


def reconcileAlbum(album, artist):
    """
        An implementated function specifically reconcile album from one artist
    """
    return reconcile(album, '/music/album', '/music/album/artist:{0}'.format(artist))


def reconcileArtist(artist, anyAlbum=None):
    """
        An implementated function specifically reconcile artist
    """
    if anyAlbum:
        anyAlbum = '/music/artist/album: ' + anyAlbum
    return reconcile(artist, '/music/artist', anyAlbum)


def rdfLookup(mid):
    """
        RDF look up API will return a RDF file describing the entity with this mid
        return a list of 3-item tuples
    """
    url = rdf_url + mid
    try:
        r = requests.get(url)
        return r.text
    except requests.RequestException:
        # if error happens, return an empty string
        return ""


def topicLookup(mid, filter):
    """
        Topic look up API of freebase
    """
    url = topic_url + mid
    try:
        r = requests.get(url, params={
            'filter': filter
        })
        return r.text
    except requests.RequestException:
        # if error happens, return an empty string
        return ""


def isAlbumSingle(rdf):
    """
        checking whether the rdf of the album shows it has a release type of single
        instead of album or EP
    """
    single = 'm.014k0b'
    return single in rdf


def checkAlbumSingle(album, artist):
    mid = reconcileAlbum(album, artist)
    if mid:
        return isAlbumSingle(rdfLookup(mid))
    return False


def getArtistWikiLink(artist, anyAlbum=None):
    mid = reconcileArtist(artist, anyAlbum)
    if mid:
        filter = '/type/object/key'
        pattern = r'/wikipedia/en_id/(\d+)\"'
        url = 'http://en.wikipedia.org/wiki/index.html?curid='
        topic = topicLookup(mid, filter)
        match = re.search(pattern, topic)
        if match:
            return url + match.group(1)
    return None


def getArtistProfile(name):
    query_string = u"""
    {{
      "name": "{}",
      "mid": null,
      "type": "/music/artist",
      "/common/topic/official_website": null,
      "/people/person/date_of_birth": null,
      "/people/person/place_of_birth": null,
      "/type/object/key": [{{
        "namespace": "/authority/musicbrainz/artist",
        "value": null,
        "optional": "optional"
      }}],
      "ns0:/type/object/key": [{{
        "namespace": "/wikipedia/en_id",
        "value": null
      }}],
      "/music/artist/album": [{{
        "/music/album/release_type!=": "Single",
        "/music/album/release_date": null,
        "/music/album/release_date>=": "2000-01-01",
        "name": null,
        "mid": null,
        "/award/award_winning_work/awards_won": [{{
          "year": null,
          "award": null,
          "optional": "optional"
        }}]
      }}],
      "/award/award_winner/awards_won": [{{
        "year": null,
        "award": null,
        "optional": "optional"
      }}],
      "/influence/influence_node/influenced_by": [],
      "/influence/influence_node/influenced": []
    }}
    """.format(name)
    backup = u"""
    {{
      "name": null,
      "/common/topic/alias": "{}",
      "mid": null,
      "type": "/music/artist",
      "/common/topic/official_website": null,
      "/people/person/date_of_birth": null,
      "/people/person/place_of_birth": null,
      "/type/object/key": [{{
        "namespace": "/authority/musicbrainz/artist",
        "value": null,
        "optional": "optional"
      }}],
      "ns0:/type/object/key": [{{
        "namespace": "/wikipedia/en_id",
        "value": null
      }}],
      "/music/artist/album": [{{
        "/music/album/release_type!=": "Single",
        "/music/album/release_date": null,
        "/music/album/release_date>=": "2000-01-01",
        "name": null,
        "mid": null,
        "/award/award_winning_work/awards_won": [{{
          "year": null,
          "award": null,
          "optional": "optional"
        }}]
      }}],
      "/award/award_winner/awards_won": [{{
        "year": null,
        "award": null,
        "optional": "optional"
      }}],
      "/influence/influence_node/influenced_by": [],
      "/influence/influence_node/influenced": []
    }}

    """.format(name)
    try:
        response = requests.get(mqlread_url, params = {
            "key": api_key,
            "query": query_string,
            "uniqueness_failure": "soft"
        })
        res = json.loads(response.text)
        if 'result' in res and res['result']:
            return res['result']
        else:
            response = requests.get(mqlread_url, params={
                "key": api_key,
                "query": backup,
                "uniqueness_failure": "soft"
            })
            res = json.loads(response.text)
            if 'result' in res and res['result']:
                return res['result']
            else:
                raise BaseException(res)
    except BaseException as e:
        raise e