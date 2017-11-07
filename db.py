from sqlalchemy import Column, Integer, String, Boolean, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

Base = declarative_base()


class Tweet(Base):
    __tablename__ = 'tweets'

    id = Column(Integer, primary_key=True)
    text = Column(String)
    created_at = Column(String)
    meta_data = Column(String)
    source = Column(String)
    truncated = Column(Boolean)
    hashtags = Column(String)
    quote_count = Column(Integer, nullable=True)
    reply_count = Column(Integer, nullable=True)
    retweet_count = Column(Integer, nullable=True)
    favorite_count = Column(Integer, nullable=True)
    lang = Column(String)

    @staticmethod
    def parse(tweet_json):
        hashtag_str = ''
        for hashtag in tweet_json['entities']['hashtags']:
            hashtag_str = hashtag_str + hashtag['text'] + ' '
        return Tweet(id=tweet_json.get('id'),
                     text=tweet_json.get('text'),
                     created_at=tweet_json.get('created_at'),
                     source=tweet_json.get('source'),
                     truncated=tweet_json.get('source'),
                     hashtags=hashtag_str,
                     quote_count=tweet_json.get('quote_count'),
                     reply_count=tweet_json.get('reply_count'),
                     retweet_count=tweet_json.get('retweet_count'),
                     favorite_count=tweet_json.get('favorite_count'),
                     lang=tweet_json.get('lang'),
                     meta_data=str(tweet_json))

    def __repr__(self):
        return '<{}, {}>: {}'.format(self.id, self.created_at, self.text)


class Hashtag(Base):
    __tablename__ = 'hashtags'

    id = Column(Integer, primary_key=True)
    text = Column(String)

    def __repr__(self):
        return '<id={}, tag={}>'.format(self.id, self.text)


class TweetTag(Base):
    __tablename__ = 'tweet_tags'

    tweet_id = Column(Integer, ForeignKey('tweets.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('hashtags.id'), primary_key=True)


class DBManager(object):

    def __init__(self, db_url, echo=False):
        self.engine = create_engine('sqlite:///{}'.format(db_url), echo=echo)
        if not database_exists(self.engine.url):
            create_database(self.engine.url)
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()

    def add(self, tweet):
        self.session.add(tweet)
        self.session.commit()

    def add_all(self, tweets):
        self.session.add_all(tweets)
        self.session.commit()

    def merge(self, tweet):
        self.session.merge(tweet)
        self.session.commit()

    def rollback(self):
        self.session.rollback()
