from sqlalchemy import and_, create_engine, MetaData, select, Table

from config import CONFIG


class MentionsStore(object):
    def __init__(self):
        self.engine = create_engine(CONFIG['db']['uri'])
        self.mentions_table = Table('mentions', MetaData(self.engine), autoload=True)

    def add_mentions(self, mentions):
        with self.engine.begin() as conn:
            for mention in mentions:
                transformed_mention = self.get_mention_from_status(mention)
                self._update_or_insert_mention(conn, transformed_mention)

    @staticmethod
    def get_mention_from_status(status):
        return {
            "id": status.id,
            'user_id': status.user.id,
            'user_screen_name': status.user.screen_name,
            'text': status.text,
            'created_at': status.created_at_in_seconds
        }

    def _update_or_insert_mention(self, conn, mention):
        if self._get_mention_from_db(conn, mention['id']):
            self._update_mention(conn, mention)
        else:
            self._insert_mention(conn, mention)

    def _get_mention_from_db(self, conn, mention_id):
        return conn.execute(self.mentions_table.select().where(
            self.mentions_table.c.id == mention_id
        )).fetchone()

    def _update_mention(self, conn, mention):
        conn.execute(self.mentions_table.update().where(
            self.mentions_table.c.id == mention['id']
        ), **mention)

    def _insert_mention(self, conn, mention):
        conn.execute(self.mentions_table.insert(), **mention)
