__author__ = 'zhoutuoyang'
import json
import requests

try:
    with open('google_api_key.txt') as f:
        api_key = f.read()
except IOError:
    print "There is something wrong with api key file."
    exit()

service_url = 'https://www.googleapis.com/freebase/v1/'
rdf_url = service_url + 'rdf'
reconciliation_url = service_url + 'reconcile'
params = {
    'key': api_key
}


def reconcile(name, kind, prop):
    """
        return mid of matched enitity or first candidate in the array.
        if candidate contains nothing or there is an error or a warning, return empty string
        if requests throws out error, return empty string as well
    """
    # process arguments
    params['name'] = name
    params['kind'] = kind
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
        A implementated function specifically reconcile album from one artist
    """
    return reconcile(album, '/music/album', '/music/album/artist:{0}'.format(artist))


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
