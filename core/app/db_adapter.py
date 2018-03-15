import psycopg2
import psycopg2.extensions
from logger import logger

LOG = logger.LOG


class LoggingCursor(psycopg2.extensions.cursor):
    def execute(self, sql: str, args=None):
        if args is not None:
            LOG.debug("SQL >\n\t> " + sql.replace("%s", "%r") % args, filepath_print_stack_level=-4)
        else:
            LOG.debug("SQL >\n\t> " + sql, filepath_print_stack_level=-4)
        try:
            psycopg2.extensions.cursor.execute(self, sql, args)
            return True
        except Exception as exc:
            LOG.error("%s: %s" % (exc.__class__.__name__, exc))
        return False


class MyPgConnection(object):
    def __init__(self):
        self._db = None

    def init(self, dbname, user, passwd, host):
        if self._db:
            LOG.debug("Try to reinit current connection: {}".format(self._db))
        dsn = "dbname={} user={} password={} host={}".format(dbname, user, passwd, host)
        LOG.info("Connect to DB:{}".format(dsn))
        self._db = psycopg2.connect(dsn=dsn)

    @property
    def cursor(self):
        """
        :return: pg cursor
        :raise: not safe
        """
        return self._db.cursor(name=None, cursor_factory=LoggingCursor, withhold=False)

    @property
    def connection(self):
        return self._db


if __name__ == '__main__':
    query_test = "INSERT INTO mycapp.users(fsusername, fspassword, fsemail, firole_id) VALUES( %s, %s, %s, %s); COMMIT"
    param_test = ("user_test", "as12sadasd", "y@er121e.vt", 123)
    # wrapper.execute(query_test, param_test)
    dsn_t = 'dbname={} user={} password={} host={}'.format(
        "mycapp",
        "local_test",
        "test",
        "127.0.0.1"
    )
    pg_conn_t = psycopg2.connect(dsn=dsn_t)
    cur_t = pg_conn_t.cursor()
    cur_t.execute(query_test, param_test)
    print(type(cur_t))
