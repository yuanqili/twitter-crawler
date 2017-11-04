from utilities import print_json
from AppAuthClient import Client
from db import DBManager, Tweet

from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from time import localtime, strftime
import pause
from datetime import datetime

CONSUMER_KEY = 'GcVofuJBUpOv6LKLLkHf9Y79e'
CONSUMER_SECRET = 'Sv7W2KEWePjJqIeKwsj7QV4hxU0Svux0WxGm70DbfCktTqQMqI'

DB_PATH = '/Users/yuanqili/Development/TwitterScrapper/tweets.sqlite'


if __name__ == '__main__':
    client = Client(CONSUMER_KEY, CONSUMER_SECRET)
    db = DBManager(DB_PATH)

    i = 0
    while 1:
        i += 1
        print('query: {}'.format(i))
        min_id = db.session.query(func.min(Tweet.id)).scalar() - 1
        tweets = client.search_tweets(q='apple', count=100, result_type='recent', max_id=min_id)

        if 'statuses' not in tweets:
            limit = client.rate_limit_status()
            reset = int(limit['resources']['search']['/search/tweets']['reset'])
            print('sleep until {}'.format(strftime("%a, %d %b %Y %H:%M:%S", localtime(reset))))
            # pause.until(reset)
            pause.minutes(2)
            continue

        for tweet in tweets['statuses']:
            try:
                db.add(Tweet(id=tweet['id'],
                             created_at=tweet['created_at'],
                             text=tweet['text'],
                             meta_data=str(tweet)))
            except IntegrityError as err:
                print(err)
                db.rollback()

    status = client.rate_limit_status()
    print_json(status)
