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
