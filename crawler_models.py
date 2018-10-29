from datetime import datetime
from sqlalchemy import BigInteger, Column, DateTime, String, Boolean
from database import Base


class MentionsCrawlRequest(Base):
    __tablename__ = 'mentions_crawl_request'
    id = Column(String(50), primary_key=True)
    mentioned_screen_name = Column(String(50))
    first_id = Column(BigInteger())
    last_id = Column(BigInteger())
    in_process = Column(Boolean(), default=False)
    last_fulfilled = Column(DateTime)
    recurring = Column(Boolean(), default=False)
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

    def __repr__(self):
        return '<MentionsCrawlRequest {}: {}>'.format(self.mentioned_screen_name, self.id)

    def to_dict(self):
        properties = [
            'mentioned_screen_name',
            'first_id',
            'last_id',
            'in_process',
            'last_fulfilled',
            'recurring',
        ]
        dict_rep = {'id': self.id}
        for property in properties:
            dict_rep[property] = getattr(self, property)
        return dict_rep

    def mark_as_processing(self):
        self.in_process = True
