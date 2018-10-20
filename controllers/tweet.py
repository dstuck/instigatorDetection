from database import db_session
from models import Tweet

class TweetController(object):

    @staticmethod
    def add_or_update_tweet_from_api(twitter_status):
        tweet = Tweet.from_twitter_status(twitter_status)
        return TweetController.add_or_update_tweet(tweet)

    @staticmethod
    def add_or_update_tweet(tweet):
        merged_tweet = db_session.merge(tweet)
        db_session.commit()
        return merged_tweet

    @staticmethod
    def get_tweet_for_id(tweet_id):
        return db_session.query(Tweet).filter_by(id=tweet_id).one_or_none()
