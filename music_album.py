__author__ = 'zhoutuoyang'
import urllib2
import json
from bs4 import BeautifulSoup
def scrap(url):
    try:
        soup = BeautifulSoup(urllib2.urlopen(url))
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
