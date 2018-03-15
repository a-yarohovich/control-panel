from flask_login import UserMixin, AnonymousUserMixin
from logger import logger
from . import db_conn
from . import login_manager

LOG = logger.LOG


class User(UserMixin):
    base_query = "SELECT * FROM mycapp.internal_users WHERE {0};"

    def __init__(self, **kwargs):
        self._user_id = kwargs.get('user_id', None)
        self._username = kwargs.get('username', None)
        self._email = kwargs.get('email', None)
        self._password = kwargs.get('password', None)
        self._about = kwargs.get('about', None)

    def get_id(self):
        return self._user_id

    def can(self) -> bool:
        return True

    def is_administrator(self) -> bool:
        return self.can()

    def __repr__(self):
        return '<User {}>'.format(self._username)

    def verify_password(self, passwd):
        return True if passwd == self._password else False

    @staticmethod
    def get_user_by_id(user_id):
        return User.get_user_by_query(User.base_query.format("fiuser_id=%s"), (user_id,))

    @staticmethod
    def get_user_by_email(email):
        return User.get_user_by_query(User.base_query.format("fsemail=%s"), (email,))

    @staticmethod
    def get_user_by_name(username):
        return User.get_user_by_query(User.base_query.format("fsusername=%s"), (username,))

    @staticmethod
    def get_user_by_query(query, params):
        cursor = db_conn.cursor
        cursor.execute(query, params)
        data = cursor.fetchone()
        if not data:
            return None
        return User(
            user_id=data[0],
            username=data[1],
            email=data[2],
            password=data[3],
            about=data[4]
        )


class AnonymousUser(AnonymousUserMixin):
    def can(self):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.get_user_by_id(user_id)
