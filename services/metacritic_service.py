__author__ = 'zhoutuoyang'
import urllib2
import urllib
import json
import unidecode
import Levenshtein
from bs4 import BeautifulSoup


metacritic = "http://www.metacritic.com"
_TIMEOUT = 60

def getAlbumUrls(album_name):
    base_url = metacritic + "/search/album/{0}/results"
    result = []
    try:
        # convert album name to ascii version
        album_name = unidecode.unidecode(album_name)
        # replace all spaces with '+' signs
        # remove all '/' signs
        url = base_url.format(album_name.replace(' ', '+').replace('/', ''))
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
    except BaseException as e:
        print u'Did not get {0} album candidate urls'.format(album_name)
        print e
    return result


def getArtistUrl(artist_name):
    base_url = metacritic + "/search/person/{0}/results"
    try:
        # convert artist name to ascii version
        converted_name = unidecode.unidecode(artist_name)
        # replace spaces with pluses
        # $ with s
        converted_name = converted_name\
                            .replace('+', ' ')\
                            .replace('!', ' ')\
                            .replace('$', 's')\
                            .replace('/', ' ')\
                            .replace('\\', ' ')\
                            .replace('&', ' ')
        url = base_url.format(urllib.quote_plus(converted_name))
        soup = BeautifulSoup(urllib2.urlopen(url, timeout=_TIMEOUT))
        # get all corresponding tags
        candidates = soup.find_all('h3', class_='product_title')
        # do string match
        table = []
        for candidate in candidates:
            titleTag = candidate.a
            can_name = titleTag.get_text().strip()
            can_url = metacritic + titleTag.get('href')
            table.append((Levenshtein.distance(artist_name, can_name), can_name, can_url))
        # sort based on distance
        table.sort(key=lambda tup: tup[0])
        # if table is not None
        # return URL
        if table:
            return table[0][2]
    except BaseException as e:
        print e


def scrapeAlbumPage(url):
    try:
        soup = BeautifulSoup(urllib2.urlopen(url, timeout=_TIMEOUT))
    except (urllib2.URLError, urllib2.HTTPError) as e:
        raise e
    infoDiv = soup.find('div', itemtype='http://schema.org/MusicAlbum', itemscope=True)
    albumTag = infoDiv.find('span', itemprop='name')
    singerTag = infoDiv.find('span', class_='band_name')
    releaseDate = infoDiv.find('span', itemprop='datePublished')
    metascore = infoDiv.select('div.metascore_w.xlarge.album')[0]
    userscore = infoDiv.select('div.metascore_w.large.user.album')[0]
    profile = {}
    profile['artist'] = singerTag.get_text().strip()
    profile['album'] = albumTag.get_text().strip()
    profile['releaseDate'] = releaseDate.get_text().strip()
    profile['metascore'] = metascore.get_text().strip()
    profile['userscore'] = userscore.get_text().strip()
    profile['criticReviews'] = []
    profile['userReviews'] = []

    criticReviews = infoDiv.select('li.review.critic_review')
    for review in criticReviews:
        sourceTag = review.find('div', class_='source').a
        gradeTag = review.find('div', class_='review_grade')
        reviewTag = review.find('div', class_='review_body')
        profile['criticReviews'].append({
            'source': sourceTag.get_text().strip(),
            'grade': gradeTag.get_text().strip(),
            'review': reviewTag.get_text().strip()
        })
    userReviews = infoDiv.select('li.review.user_review')
    for review in userReviews:
        gradeTag = review.find('div', class_='review_grade')
        reviewColTag = review.find('span', class_='blurb_collapsed')
        reviewExpTag = review.find('span', class_='blurb_expanded')
        profile['userReviews'].append({
            'grade': gradeTag.get_text().strip(),
            'review': (reviewColTag.get_text() + reviewExpTag.get_text()).strip()
        })
    return json.dumps(profile, indent=4)


def scrapeArtistPage(url):
    try:
        soup = BeautifulSoup(urllib2.urlopen(url + '?filter-options=music', timeout=_TIMEOUT))
    except (urllib2.URLError, urllib2.HTTPError) as e:
        raise e
    artist_name = soup.find('div', class_='person_title').get_text().strip()
    albumRows = soup.find('table', class_='credits').find('tbody').find_all('tr')
    albums = []
    for row in albumRows:
        nameTag = row.find('td', class_='title')
        name = nameTag.a.get_text()
        url = metacritic + nameTag.a.get('href')
        releaseDate = row.find('td', class_='year').get_text().strip()
        albums.append((name, releaseDate, url))
    return (artist_name, albums)
