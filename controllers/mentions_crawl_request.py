from datetime import datetime
from uuid import uuid4

from sqlalchemy import or_

from database import db_session
from crawler_models import MentionsCrawlRequest

class MentionsCrawlRequestController(object):
    @staticmethod
    def get_mentions_crawl_request_for_id(request_id):
        return db_session.query(MentionsCrawlRequest).filter_by(id=request_id).one_or_none()

    @staticmethod
    def create_mentions_crawl_request(mentioned_screen_name, recurring=False):
        mentions_crawl_request = MentionsCrawlRequest(
            id=uuid4().hex,
            mentioned_screen_name=mentioned_screen_name,
            recurring=recurring
        )
        db_session.add(mentions_crawl_request)
        db_session.commit()
        return mentions_crawl_request

    @staticmethod
    def get_requests_ready_for_processing():
        return db_session.query(MentionsCrawlRequest).filter(
            MentionsCrawlRequest.in_process == False
        ).filter(
            or_(MentionsCrawlRequest.last_fulfilled == None, MentionsCrawlRequest.recurring == True)
        ).all()

    @staticmethod
    def update_request_as_processed(request_id, last_id, first_id=None):
        crawl_request = MentionsCrawlRequestController.get_mentions_crawl_request_for_id(request_id)
        crawl_request.last_fulfilled = datetime.utcnow()
        crawl_request.in_process = False
        crawl_request.last_id = last_id
        if first_id:
            crawl_request.first_id = first_id
        db_session.add(crawl_request)
        db_session.commit()
        return crawl_request
