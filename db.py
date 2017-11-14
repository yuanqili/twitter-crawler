from sqlalchemy import Column, Integer, String, Boolean, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy_utils import database_exists, create_database

from newspaper import Article

Base = declarative_base()


class Tweet(Base):
    __tablename__ = 'tweets'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    news_id = Column(Integer, ForeignKey('newses.id'))
    created_at = Column(String)
    text = Column(String)
    source = Column(String)
    truncated = Column(Boolean)
    hashtags = Column(String)
    quote_count = Column(Integer, nullable=True)
    reply_count = Column(Integer, nullable=True)
    retweet_count = Column(Integer, nullable=True)
    favorite_count = Column(Integer, nullable=True)
    lang = Column(String)
    url = Column(String)
    meta_data = Column(String)

    user = relationship('User', back_populates='tweets')
    news = relationship('News', back_populates='tweets')

    @staticmethod
    def parse(tweet_json):
        url = ''
        try:
            url = tweet_json.get('entities')['urls'][0]['url']
        except IndexError as err:
            pass
        # if url is not '':
        #     print(url)
        return Tweet(id=tweet_json.get('id'),
                     user_id=tweet_json.get('user')['id'],
                     text=tweet_json.get('text'),
                     created_at=tweet_json.get('created_at'),
                     source=tweet_json.get('source'),
                     truncated=tweet_json.get('truncated'),
                     hashtags=','.join([tag['text'] for tag in tweet_json['entities']['hashtags']]),
                     quote_count=tweet_json.get('quote_count'),
                     reply_count=tweet_json.get('reply_count'),
                     retweet_count=tweet_json.get('retweet_count'),
                     favorite_count=tweet_json.get('favorite_count'),
                     lang=tweet_json.get('lang'),
                     url=url,
                     meta_data=str(tweet_json))

    def __repr__(self):
        return f'<{self.id}, {self.created_at}>: {repr(self.text)}'


# class Hashtag(Base):
#     __tablename__ = 'hashtags'
#
#     id = Column(Integer, primary_key=True)
#     text = Column(String)
#
#     def __repr__(self):
#         return '<id={}, tag={}>'.format(self.id, self.text)


# class TweetTag(Base):
#     __tablename__ = 'tweet_tags'
#
#     tweet_id = Column(Integer, ForeignKey('tweets.id'), primary_key=True)
#     tag_id = Column(Integer, ForeignKey('hashtags.id'), primary_key=True)


class News(Base):
    __tablename__ = 'newses'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    text = Column(String)
    url = Column(String)

    tweets = relationship('Tweet', back_populates='news')

    @staticmethod
    def parse(link):
        try:
            article = Article(link)
            article.download()
            article.parse()
            return News(title=article.title, text=article.text, url=link)
        except Exception:
            return None


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    screen_name = Column(String)
    description = Column(String)

    tweets = relationship('Tweet', back_populates='user')

    @staticmethod
    def parse(user_json):
        return User(id=user_json.get('id'),
                    name=user_json.get('name'),
                    screen_name=user_json.get('screen_name'),
                    description=user_json.get('description'))

    def __repr__(self):
        return f'<{self.name}>'


class DBManager(object):

    def __init__(self, db_url, echo=False):
        self.engine = create_engine(f'sqlite:///{db_url}', echo=echo)
        if not database_exists(self.engine.url):
            create_database(self.engine.url)
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()

    def add(self, item):
        self.session.add(item)
        self.session.commit()

    def add_all(self, items):
        self.session.add_all(items)
        self.session.commit()

    def merge(self, item):
        self.session.merge(item)
        self.session.commit()

    def rollback(self):
        self.session.rollback()
