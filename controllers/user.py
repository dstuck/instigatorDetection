from database import db_session
from models import User

class UserController(object):
    @staticmethod
    def add_or_update_user_from_api(api_user):
        user = User.from_twitter_user(api_user)
        return UserController.add_or_update_user(user)

    @staticmethod
    def add_or_update_user(new_user):
        new_user = UserController.get_or_update_user(new_user)
        db_session.add(new_user)
        db_session.commit()
        return new_user

    @staticmethod
    def get_or_update_user(user):
        merged_user = db_session.merge(user)
        db_session.commit()
        return merged_user

    @staticmethod
    def get_user_for_id(user_id):
        return db_session.query(User).filter_by(id=user_id).one_or_none()

    @staticmethod
    def get_user_for_screen_name(screen_name):
        return db_session.query(User).filter_by(screen_name=screen_name).one_or_none()

    @staticmethod
    def get_or_create_user_for_id(user_id):
        new_user = UserController.get_user_for_id(user_id)
        if new_user is None:
            new_user = User(id=user_id)
        return new_user

    @staticmethod
    def add_followers_by_id(user, follower_id_list):
        new_followers = set()
        for follower_id in follower_id_list:
            follower_user = UserController.get_or_create_user_for_id(follower_id)
            new_followers.add(follower_user)
        user.followers.update(new_followers)
        db_session.commit()

    @staticmethod
    def add_friends_by_id(user, friend_id_list):
        new_friends = set()
        for friend_id in friend_id_list:
            friend_user = UserController.get_or_create_user_for_id(friend_id)
            new_friends.add(friend_user)
        user.friends.update(new_friends)
        db_session.commit()
