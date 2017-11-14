import configparser
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import localtime, strftime

import pause

from db import DBManager, Tweet, User, News
from twitter import TwitterClient

# Reads config parameters
config = configparser.ConfigParser()
config.read('config')
TWITTER_KEY = config.get('twitter', 'key')
TWITTER_SECRET = config.get('twitter', 'secret')
TWITTER_ACCOUNTS = config.get('external files', 'twitter_account_path')
DB_PATH = config.get('external files', 'db_path')
DB_FILE = config.get('external files', 'db_file')

# Reads Twitter accounts
twitter_accounts = []
with open(TWITTER_ACCOUNTS, 'r') as f:
    line = f.readline()
    while line:
        line = line.strip()
        account = line[1:] if line[0] == '@' else line
        twitter_accounts.append(account)
        line = f.readline()


# Worker for parsing tweet (tweet, user, news) rows in database
def parse_tweet(response):
    tweet = Tweet.parse(response)
    user = User.parse(response['user'])
    news = News.parse(tweet.url)
    return tweet, user, news


def tweets_search(query, iteration=0, show=False):
    client = TwitterClient(TWITTER_KEY, TWITTER_SECRET)
    db = DBManager(os.path.join(DB_PATH, DB_FILE))

    i = 0
    while iteration == 0 or i != iteration:
        i += 1
        print(f'round {i} of query <{query}>')
        # min_id = min_id - 1 if min_id else None
        # min_id = db.session.query(Tweet).filter_by(user_id=)
        min_id = None if i == 1 else min_id
        tweets = client.search_tweets(q=query, result_type='recent', lang='en', max_id=min_id)

        # If exceeds rate limit, wait until reset
        # Seems not working properly, to be fixed
        if 'statuses' not in tweets:
            limit = client.rate_limit_status()
            reset = int(limit['resources']['search']['/search/tweets']['reset'])
            print('sleep until {}'.format(strftime("%a, %d %b %Y %H:%M:%S", localtime(reset))))
            # pause.until(reset)
            pause.minutes(2)
            print('continue scraping')
            continue

        # Breaks if all have been scraped
        if len(tweets['statuses']) == 0:
            break

        # Adds tweets into database (multi-threading)
        with ThreadPoolExecutor(max_workers=20) as executor:
            future_results = [executor.submit(parse_tweet, tweet) for tweet in tweets['statuses']]
            for future in as_completed(future_results):
                try:
                    tweet, user, news = future.result()
                    if news is not None:
                        tweet.news = news
                        # db.merge(news)
                    db.merge(tweet)
                    db.merge(user)
                    min_id = min(min_id, tweet.id) if min_id else tweet.id
                except Exception as err:
                    print(err)
                else:
                    if show:
                        print(repr(tweet))


if __name__ == '__main__':
    for account in twitter_accounts:
        tweets_search(f'from:{account} filter:links', 10, True)
