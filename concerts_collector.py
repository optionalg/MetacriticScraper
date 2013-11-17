__author__ = 'zhoutuoyang'

import json
from services import songkick_service

if __name__ == '__main__':
    # get 3000 upcoming events if there are
    events = songkick_service.getUpcomingEvents(pages=60)
    with open('songkick.json', mode='w', buffering=1) as f:
        f.write(json.dumps(events, indent=4))
        f.flush()