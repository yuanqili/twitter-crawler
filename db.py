from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Tweet(Base):
    __tablename__ = 'tweets'

    id = Column(Integer, primary_key=True)
    text = Column(String)
    created_at = Column(String)
    meta_data = Column(String)

    def __repr__(self):
        return '<{}, {}>: {}'.format(self.id, self.created_at, self.text)


class DBManager(object):

    def __init__(self, db_location):
        self.engine = create_engine('sqlite:///{}'.format(db_location))
        self.session = sessionmaker(bind=self.engine)()

    def add(self, tweet):
        self.session.add(tweet)
        self.session.commit()

    def add_all(self, tweets):
        self.session.add_all(tweets)
        self.session.commit()

    def rollback(self):
        self.session.rollback()
