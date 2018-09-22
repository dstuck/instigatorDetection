from sqlalchemy import create_engine, MetaData, Table

from config import CONFIG


class MentionsStore(object):
    _engine = None
    _mentions_table = None
    
    @classmethod
    def lazy_load_tables(cls):
        if cls._engine is None:
            cls._engine = create_engine(CONFIG['db']['uri'])
        if cls._mentions_table is None:
            cls._mentions_table = Table('mentions', MetaData(cls._engine), autoload=True)

    @classmethod
    def add_mentions(cls, mentions, mentioned_screen_name):
        cls.lazy_load_tables()
        with cls._engine.begin() as conn:
            for mention in mentions:
                transformed_mention = cls._get_mention_from_status(mention)
                transformed_mention['mentioned_screen_name'] = mentioned_screen_name
                cls._update_or_insert_mention(conn, transformed_mention)

    @staticmethod
    def _get_mention_from_status(status):
        return {
            "id": status.id,
            'user_id': status.user.id,
            'user_screen_name': status.user.screen_name,
            'text': status.text,
            'created_at': status.created_at_in_seconds
        }

    @classmethod
    def _update_or_insert_mention(cls, conn, mention):
        if cls._get_mention_from_db(conn, mention['id']):
            cls._update_mention(conn, mention)
        else:
            cls._insert_mention(conn, mention)

    @classmethod
    def _get_mention_from_db(cls, conn, mention_id):
        return conn.execute(cls._mentions_table.select().where(
            cls._mentions_table.c.id == mention_id
        )).fetchone()

    @classmethod
    def _update_mention(cls, conn, mention):
        conn.execute(cls._mentions_table.update().where(
            cls._mentions_table.c.id == mention['id']
        ), **mention)

    @classmethod
    def _insert_mention(cls, conn, mention):
        conn.execute(cls._mentions_table.insert(), **mention)

    @classmethod
    def find_latest_mention_for_user(cls, user_screen_name):
        """

        :param user_screen_name: Screen name of user
        :return: Integer timestamp of latest stored mention
        """
        cls.lazy_load_tables()
        row = cls._mentions_table.select().where(
            cls._mentions_table.c.mentioned_screen_name == user_screen_name
        ).order_by(
            cls._mentions_table.c.created_at.desc()
        ).limit(1).execute().fetchone()
        return dict(row)
