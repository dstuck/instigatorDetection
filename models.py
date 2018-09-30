from calendar import timegm
from datetime import datetime
from email.utils import parsedate

from sqlalchemy import BigInteger, Column, DateTime, Integer, ForeignKey, String, Table
from sqlalchemy.orm import relationship
from database import Base


# association table
tweet_mentions = Table(
    'tweet_mentions',
    Base.metadata,
    Column('tweet_id', ForeignKey('tweets.id'), primary_key=True),
    Column('user_id', ForeignKey('users.id'), primary_key=True)
)


class User(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    screen_name = Column(String(50), unique=True)
    created_at = Column(Integer())
    followers_count = Column(BigInteger())
    favorites_count = Column(BigInteger())
    statuses_count = Column(BigInteger())
    lang = Column(String(20))
    description = Column(String(320))
    name = Column(String(200))
    db_created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )
    db_updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    tweets = relationship("Tweet", order_by="desc(Tweet.id)", back_populates="user")
    mentions = relationship(
        "Tweet",
        secondary=tweet_mentions,
        back_populates="mentioned_users"
    )

    def __repr__(self):
        return '<User {}, {}>'.format(self.screen_name, self.id)

    @classmethod
    def from_twitter_user(cls, twitter_user):
        init_kwargs = {
            'id': twitter_user.id,
            'screen_name': twitter_user.screen_name,
            'created_at': timegm(parsedate(twitter_user.created_at)) if twitter_user.created_at else None,
            'followers_count': twitter_user.followers_count,
            'favorites_count': twitter_user.favourites_count,
            'statuses_count': twitter_user.statuses_count,
            'lang': twitter_user.lang,
            'description': twitter_user.description,
            'name': twitter_user.name,
        }
        return cls(**init_kwargs)


class Tweet(Base):
    __tablename__ = 'tweets'
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.id'))
    created_at = Column(Integer())
    text = Column(String(320))
    lang = Column(String(20))
    in_reply_to_tweet_id = Column(BigInteger)
    in_reply_to_user_id = Column(BigInteger)
    db_created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )
    db_updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    user = relationship("User", back_populates="tweets")
    mentioned_users = relationship(
        "User",
        secondary=tweet_mentions,
        back_populates="mentions"
    )

    def __repr__(self):
        return '<Tweet @{}: {}>'.format(self.user.screen_name, self.text)

    @classmethod
    def from_twitter_status(cls, tweet_status):
        init_kwargs = {
            'id': tweet_status.id,
            'user_id': tweet_status.user.id,
            'created_at': tweet_status.created_at_in_seconds,
            'text': tweet_status.text,
            'lang': tweet_status.lang,
            'in_reply_to_tweet_id': tweet_status.in_reply_to_status_id,
            'in_reply_to_user_id': tweet_status.in_reply_to_user_id,
        }
        tweet = cls(**init_kwargs)
        tweet.user = User.from_twitter_user(tweet_status.user)
        for m_user in tweet_status.user_mentions:
            tweet.mentioned_users.append(User.from_twitter_user(m_user))
        return tweet
