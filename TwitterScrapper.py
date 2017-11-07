from time import localtime, strftime

import pause
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from AppAuthClient import Client
from db import DBManager, Tweet

CONSUMER_KEY = 'GcVofuJBUpOv6LKLLkHf9Y79e'
CONSUMER_SECRET = 'Sv7W2KEWePjJqIeKwsj7QV4hxU0Svux0WxGm70DbfCktTqQMqI'

DB_PATH = '/path/to/db/db-name.sqlite'


def tweets_search(query):
    client = Client(CONSUMER_KEY, CONSUMER_SECRET)
    db = DBManager(DB_PATH)

    i = 0
    while True:
        i += 1
        print('query: {}'.format(i))
        min_id = db.session.query(func.min(Tweet.id)).scalar()
        min_id = min_id - 1 if min_id else None
        tweets = client.search_tweets(q=query, result_type='recent', lang='en', max_id=min_id)

        # If exceeds rate limit, wait until reset
        # Seems not working properly, to be fixed
        if 'statuses' not in tweets:
            limit = client.rate_limit_status()
            reset = int(limit['resources']['search']['/search/tweets']['reset'])
            print('sleep until {}'.format(strftime("%a, %d %b %Y %H:%M:%S", localtime(reset))))
            # pause.until(reset)
            pause.minutes(2)
            continue

        # Adds tweets into database
        for tweet in tweets['statuses']:
            try:
                db.add(Tweet.parse(tweet))
            except IntegrityError as err:
                print(err)
                db.rollback()


if __name__ == '__main__':
    tweets_search('apple')
