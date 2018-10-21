from uuid import uuid4

from database import db_session
from models import Cohort

class CohortController(object):
    @staticmethod
    def create_cohort_from_users(users, description=''):
        new_cohort = Cohort(
            id=uuid4().int % 100000000,
            description=description,
            members=set(users)
        )
        db_session.add(new_cohort)
        db_session.commit()
        return new_cohort

    @staticmethod
    def get_cohort_for_id(cohort_id):
        return db_session.query(Cohort).filter_by(id=cohort_id).one_or_none()
