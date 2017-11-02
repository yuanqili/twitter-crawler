import json
from utilities import print_json
from AppAuthClient import Client
from db import DBManager, Tweet

from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

CONSUMER_KEY = 'GcVofuJBUpOv6LKLLkHf9Y79e'
CONSUMER_SECRET = 'Sv7W2KEWePjJqIeKwsj7QV4hxU0Svux0WxGm70DbfCktTqQMqI'

DB_PATH = '/Users/yuanqili/Development/TwitterScrapper/tweets.sqlite'


if __name__ == '__main__':
    client = Client(CONSUMER_KEY, CONSUMER_SECRET)
    db = DBManager(DB_PATH)

    for i in range(100):
        print('query {}'.format(i))
        min_id = db.session.query(func.min(Tweet.id)).scalar() - 1
        tweets = client.search_tweets(q='apple', count=100, result_type='recent', max_id=min_id)
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
