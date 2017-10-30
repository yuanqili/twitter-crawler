import json
from AppAuthClient import Client

CONSUMER_KEY = 'GcVofuJBUpOv6LKLLkHf9Y79e'
CONSUMER_SECRET = 'Sv7W2KEWePjJqIeKwsj7QV4hxU0Svux0WxGm70DbfCktTqQMqI'

if __name__ == '__main__':
    client = Client(CONSUMER_KEY, CONSUMER_SECRET)
    # tweet = client.request(
    #     'https://api.twitter.com/1.1/statuses/show.json?id=316683059296624640')
    # print(json.dumps(tweet, sort_keys=True, indent=4, separators=(',', ':')))

    tweets = client.search_tweets(q='apple', count=100)
    print(json.dumps(tweets, sort_keys=True, indent=4, separators=(',', ':')))

    status = client.rate_limit_status()
    print(json.dumps(status, sort_keys=True, indent=4, separators=(',', ':')))
