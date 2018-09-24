from calendar import timegm
from email.utils import parsedate

from sqlalchemy import Column, BigInteger, Integer, String
from database import Base



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

    def __repr__(self):
        return '<User {}, {}>'.format(self.screen_name, self.id)

    @classmethod
    def from_twitter_user(cls, twitter_user):
        init_kwargs = {
            'id': twitter_user.id,
            'screen_name': twitter_user.screen_name,
            'created_at': timegm(parsedate(twitter_user.created_at)),
            'followers_count': twitter_user.followers_count,
            'favorites_count': twitter_user.favourites_count,
            'statuses_count': twitter_user.statuses_count,
            'lang': twitter_user.lang,
            'description': twitter_user.description,
            'name': twitter_user.name,
        }
        return cls(**init_kwargs)
