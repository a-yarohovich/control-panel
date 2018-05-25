from flask_login import UserMixin, AnonymousUserMixin
from logger import logger
from . import db_conn
from . import login_manager

LOG = logger.LOG


class Service(object):
    def __init__(self, fiservice_id, fiservice_status, fsserv_desc, fsserv_code):
        self.fiservice_id = fiservice_id
        self.fiservice_status = fiservice_status
        self.fsserv_desc = fsserv_desc
        self.fsserv_code = fsserv_code

    def __repr__(self):
        return '<Service {}:{}>'.format(self.fsserv_code, self.fsserv_desc)

    @staticmethod
    def from_dict(entries):
        return Service(
            entries["fiservice_id"],
            entries["fiservice_status"],
            entries["fsserv_desc"],
            entries["fsserv_code"]
        )

    @staticmethod
    def get_by_code(fsserv_code):
        with db_conn:
            cursor = db_conn.cursor
            cursor.execute("SELECT * FROM mycapp.service WHERE fsserv_code=%s", (fsserv_code,))
            data = cursor.fetchone()
            if not data:
                return None
            return Service(
                fiservice_id=data[0],
                fiservice_status=data[1],
                fsserv_desc=data[2],
                fsserv_code=data[3]
            )

    @staticmethod
    def write(fiservice_status, fsserv_desc, fsserv_code, fiservice_id=None):
        def update():
            # Update existing service
            cursor.execute(
                "UPDATE "
                "mycapp.service "
                "SET fiservice_status=%s, fsserv_desc=%s, fsserv_code=%s "
                "WHERE fiservice_id=%s",
                (fiservice_status, fsserv_desc, fsserv_code, fiservice_id)
            )

        def insert():
            # Insert new service
            cursor.execute(
                "INSERT INTO "
                "mycapp.service(fiservice_status, fsserv_desc, fsserv_code) "
                "VALUES(%s, %s, %s) "
                "RETURNING fiservice_id",
                (fiservice_status, fsserv_code, fsserv_desc)
            )
            return cursor.fetchone()[0]

        LOG.debug(
            "Try to write service: id={}, status={}, code={}, desc={}".format(
                fiservice_id, fiservice_status, fsserv_code, fsserv_desc)
        )
        with db_conn:
            cursor = db_conn.cursor
            if fiservice_id:
                update()
            else:
                fiservice_id = insert()
            return Service(
                fiservice_id=fiservice_id,
                fiservice_status=fiservice_status,
                fsserv_desc=fsserv_desc,
                fsserv_code=fsserv_code
            )

    @staticmethod
    def delete(serv_tuple_ids: tuple):
        LOG.debug(
            "Try to delete services: {}".format(serv_tuple_ids))
        if not serv_tuple_ids:
            return
        with db_conn:
            cursor = db_conn.cursor
            n = len(serv_tuple_ids)
            cursor.execute(
                "DELETE FROM mycapp.service WHERE fiservice_id IN ({}{})".format("%s," * (n - 1), "%s"),
                serv_tuple_ids
            )

    @staticmethod
    def dump() -> list:
        """
        :return: List of all services
        """
        with db_conn:
            cursor = db_conn.cursor
            cursor.execute(
                "SELECT "
                    "fiservice_id, "    
                    "fiservice_status, "         
                    "fsserv_desc, "            
                    "fsserv_code "     
                "FROM mycapp.service"
            )
            return [Service(line[0], line[1], line[2], line[3]) for line in cursor.fetchall()]


class User(UserMixin):
    base_query = "SELECT * FROM mycapp.internal_users WHERE {0};"

    def __init__(self, **kwargs):
        self._user_id = kwargs.get('user_id', None)
        self._username = kwargs.get('username', None)
        self._email = kwargs.get('email', None)
        self._password = kwargs.get('password', None)
        self._about = kwargs.get('about', None)

    def __repr__(self):
        return '<User {}>'.format(self._username)

    def get_id(self):
        return self._user_id

    def can(self) -> bool:
        return True

    def is_administrator(self) -> bool:
        return self.can()

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
        with db_conn:
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
