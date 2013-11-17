__author__ = 'zhoutuoyang'

import os
import json
import requests

try:
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'songkick_api_key.txt')) as f:
        api_key = f.read()
except IOError as e:
    print "There is something wrong with api key file."
    exit()


songkick_base_url = 'http://api.songkick.com/api/3.0/'
event_url = songkick_base_url + 'events.json'

def getUpcomingEvents(pages=50):
    params = {
        'location': 'clientip',
        'apikey': api_key,
    }
    events = []
    for page in range(1, pages + 1):
        # pagination
        params['page'] = page
        response = requests.get(event_url, params=params)
        try:
            data = json.loads(response.text)
            if data['resultsPage']['status'] == 'ok':
                results = data['resultsPage']['results']
                # checking whether the result is empty or not
                # if empty, all entries has been covered, exit
                if results:
                    events += results['event']
                else:
                    break;
        except BaseException as e:
            print e
    return events