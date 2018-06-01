import datetime
from flask_login import UserMixin, AnonymousUserMixin
from logger import logger
from . import db_conn
from . import login_manager

LOG = logger.LOG


class Product(object):
    def __init__(self, fiproduct_id, fiaccount_id, filimit_user_profiles, fistatus, fdcreation, fdclose_date):
        self.fiproduct_id: int = fiproduct_id
        self.fiaccount_id: int = fiaccount_id
        self.filimit_user_profiles: int = filimit_user_profiles
        self.fistatus: int = fistatus
        self.fdcreation: datetime.date = fdcreation
        self.fdclose_date: datetime.date = fdclose_date

    @staticmethod
    def get(fiproduct_id):
        """
        :param fiproduct_id:
        :return:
        :raise: not safe
        """
        with db_conn:
            cursor = db_conn.cursor
            cursor.execute("SELECT * from mycapp.product WHERE fiproduct_id=%s", (fiproduct_id,))
            prod_data = cursor.fetchone()
            return Product(
                fiproduct_id=prod_data[0],
                fiaccount_id=prod_data[1],
                filimit_user_profiles=prod_data[2],
                fistatus=prod_data[3],
                fdcreation=prod_data[4],
                fdclose_date=prod_data[5]
            )


class Language(object):
    def __init__(self, filang_id, fslang_iso639_1, fslang_desc):
        self.filang_id = filang_id
        self.fslang_iso639_1 = fslang_iso639_1
        self.fslang_desc = fslang_desc

    def __repr__(self):
        return "<Lang {}:{}>".format(self.filang_id, self.fslang_iso639_1)

    def __str__(self):
        return self.fslang_iso639_1

    @staticmethod
    def get(fslang_iso639_1, filang_id):
        """
        :return:
        :raise: not safe
        """
        with db_conn:
            cursor = db_conn.cursor
            if fslang_iso639_1:
                cursor.execute(
                    "SELECT "
                        "filang_id, "
                        "fslang_iso639_1, "
                        "fslang_desc "
                    "FROM mycapp.languages where fslang_iso639_1=%s",
                    (fslang_iso639_1,)
                )
            elif filang_id:
                cursor.execute(
                    "SELECT "
                        "filang_id, "
                        "fslang_iso639_1, "
                        "fslang_desc "
                    "FROM mycapp.languages where filang_id=%s",
                    (filang_id,)
                )
            else:
                raise ValueError("Missing mandatory params")
            data = cursor.fetchone()
            if not data:
                return None
            return Language(
                filang_id=data[0],
                fslang_iso639_1=data[1],
                fslang_desc=data[2]
            )

    @staticmethod
    def from_dict(entries):
        return Language(
            entries["filang_id"],
            entries["fslang_iso639_1"],
            entries["fslang_desc"]
        )

    @staticmethod
    def delete(ids_todelete: tuple):
        if not ids_todelete:
            return
        LOG.debug("Try to delete: {}".format(ids_todelete))
        with db_conn:
            cursor = db_conn.cursor
            n = len(ids_todelete)
            cursor.execute(
                "DELETE FROM mycapp.languages WHERE filang_id IN ({}{})".format("%s," * (n - 1), "%s"),
                ids_todelete
            )

    @staticmethod
    def update(filang_id, fslang_iso639_1, fslang_desc):
        LOG.debug(
            "Try to update: id={}, iso639.1={}".format(filang_id, fslang_iso639_1)
        )
        with db_conn:
            cursor = db_conn.cursor
            cursor.execute(
                "UPDATE "
                    "mycapp.languages "
                "SET fslang_iso639_1=%s, fslang_desc=%s"
                "WHERE filang_id=%s",
                (fslang_iso639_1, fslang_desc, filang_id)
            )
            return Language(
                filang_id=filang_id,
                fslang_desc=fslang_desc,
                fslang_iso639_1=fslang_iso639_1
            )

    @staticmethod
    def insert(fslang_iso639_1, fslang_desc):
        LOG.debug(
            "Try to insert new lang: iso639.1={}".format(fslang_iso639_1)
        )
        with db_conn:
            cursor = db_conn.cursor
            cursor.execute(
                "INSERT INTO "
                    "mycapp.languages(fslang_iso639_1, fslang_desc) "
                "VALUES(%s, %s) "
                "RETURNING filang_id",
                (fslang_iso639_1, fslang_desc)
            )
            filang_id = cursor.fetchone()[0]
            return Language(
                filang_id=filang_id,
                fslang_desc=fslang_desc,
                fslang_iso639_1=fslang_iso639_1
            )

    @staticmethod
    def dump() -> list:
        """
        :return: list of all lang objects
                    "filang_id,"        # [0]
                    "fslang_iso639_1,"  # [1]
                    "fslang_desc,"      # [2]
        """
        with db_conn:
            cursor = db_conn.cursor
            cursor.execute(
                "SELECT "
                    "filang_id,"        
                    "fslang_iso639_1,"  
                    "fslang_desc "      
                "FROM mycapp.languages"
            )
            return [Language(data[0], data[1], data[2]) for data in cursor.fetchall()]


class Account(object):
    def __init__(
            self,
            fiaccount_id,
            fipay_type_id,
            fdstart_date,
            fdclose_date,
            lang: Language,
            fistatus,
            fiblockcode,
            balance,
            currency
    ):
        self.fiaccount_id = fiaccount_id
        self.fipay_type_id = fipay_type_id
        self.fdstart_date = fdstart_date
        self.fdclose_date = fdclose_date
        self.lang = lang
        self.fistatus = fistatus
        self.fiblockcode = fiblockcode
        self.balance = balance
        self.currency = currency

    @staticmethod
    def dump_products(self):
        with db_conn:
            cursor = db_conn.cursor
            cursor.execute("SELECT * from mycapp.product WHERE fiaccount_id=%s", (self.fiaccount_id,))
            products = list()
            for prd in cursor:
                products.append(Product(
                    fiproduct_id=prd[0],
                    fiaccount_id=prd[1],
                    filimit_user_profiles=prd[2],
                    fistatus=prd[3],
                    fdcreation=prd[4],
                    fdclose_date=prd[5]
                ))
            return products

    @staticmethod
    def get(fiaccount_id):
        """
        :param fiaccount_id:
        :return:
        :raise: not safe
        """
        with db_conn:
            cursor = db_conn.cursor
            cursor.execute("SELECT * from mycapp.account WHERE fiaccount_id=%s", (fiaccount_id,))
            acc_data = cursor.fetchone()
            return Account(
                fiaccount_id=acc_data[0],
                fipay_type_id=acc_data[1],
                fdstart_date=acc_data[2],
                fdclose_date=acc_data[3],
                lang=Language.get(fslang_iso639_1=None, filang_id=acc_data[4]),
                fistatus=acc_data[5],
                fiblockcode=acc_data[6],
                balance=0.0, # TODO
                currency="$s" ???
            )


class CDR(object):
    def __init__(self):
        pass

    @staticmethod
    def dump(from_date, to_date) -> list:
        """
        :param from_date:
        :param to_date:
        :return: list of tuples cdrs
                    "ficontext_id, "        # cdr[0]
                    "fscall_id, "           # cdr[1]
                    "fiplatform_id, "       # cdr[2]
                    "fiproduct_id, "        # cdr[3]
                    "fiaccount_id, "        # cdr[4]
                    "fscalling_number, "    # cdr[5]
                    "fscalled_number, "     # cdr[6]
                    "facreate_time, "       # cdr[7]
                    "faanswer_time, "       # cdr[8]
                    "fadestroy_time, "      # cdr[9]
                    "fiduration, "          # cdr[10]
                    "fiend_reason, "        # cdr[11]
                    "fitariff_id, "         # cdr[12]
                    "fiprovider_id, "       # cdr[13]
                    "fiservice_code, "      # cdr[14]
                    "fsregion_prefix, "     # cdr[15]
                    "fscall_info, "         # cdr[16]
                    "fnsum "                # cdr[17]
        """
        if not from_date or not to_date:
            raise ValueError("Didn't set from_date or to_date")
        with db_conn:
            cursor = db_conn.cursor
            cursor.execute(
                "SELECT "
                    "ficontext_id, "      
                    "fscall_id, "         
                    "fiplatform_id, "     
                    "fiproduct_id, "      
                    "fiaccount_id, "      
                    "fscalling_number, "  
                    "fscalled_number, "   
                    "facreate_time, "     
                    "faanswer_time, "     
                    "fadestroy_time, "    
                    "fiduration, "        
                    "fiend_reason, "      
                    "fitariff_id, "       
                    "fiprovider_id, "     
                    "fiservice_code, "    
                    "fsregion_prefix, "   
                    "fscall_info, "       
                    "fnsum "              
                "FROM mycapp.cdr "
                "WHERE facreate_time BETWEEN '{}' AND '{}'".format(from_date, to_date)
            )
            return cursor.fetchall()


class Provider(object):
    def __init__(self, fiprovider_id, fiprov_status, fdstart_date, fdend_date, fsprovider_code, fsdesc):
        self.fiprovider_id = fiprovider_id
        self.fiprov_status = fiprov_status
        self.fdstart_date = fdstart_date
        self.fdend_date = fdend_date
        self.fsprovider_code = fsprovider_code
        self.fsdesc = fsdesc

    def __repr__(self):
        return "<Provider {}:{}>".format(self.fiprovider_id, self.fsprovider_code)

    @staticmethod
    def from_dict(entries):
        return Provider(
            entries["fiprovider_id"],
            entries["fiprov_status"],
            entries["fdstart_date"],
            entries["fdend_date"],
            entries["fsprovider_code"],
            entries["fsdesc"]
        )

    @staticmethod
    def delete(ids_todelete: tuple):
        if not ids_todelete:
            return
        LOG.debug("Try to delete provider: {}".format(ids_todelete))
        with db_conn:
            cursor = db_conn.cursor
            n = len(ids_todelete)
            cursor.execute(
                "DELETE FROM mycapp.provider WHERE fiprovider_id IN ({}{})".format("%s," * (n - 1), "%s"),
                ids_todelete
            )

    @staticmethod
    def write(fiprov_status, fdstart_date, fdend_date, fsprovider_code, fsdesc, fiprovider_id=None):
        def update():
            # Update existing service
            cursor.execute(
                "UPDATE "
                    "mycapp.provider "
                "SET fiprov_status=%s, fdstart_date=%s, fdend_date=%s, fsprovider_code=%s, fsdesc=%s"
                "WHERE fiprovider_id=%s",
                (fiprov_status, fdstart_date, fdend_date, fsprovider_code, fsdesc, fiprovider_id)
            )

        def insert():
            # Insert new service
            cursor.execute(
                "INSERT INTO "
                    "mycapp.provider(fiprov_status, fdstart_date, fdend_date, fsprovider_code, fsdesc) "
                "VALUES(%s, %s, %s, %s, %s) "
                "RETURNING fiprovider_id",
                (fiprov_status, fdstart_date, fdend_date, fsprovider_code, fsdesc)
            )
            return cursor.fetchone()[0]

        LOG.debug(
            "Try to write provider: id={}, status={}, code={}, desc={}".format(
                fiprovider_id, fiprov_status, fsprovider_code, fsdesc)
        )
        with db_conn:
            cursor = db_conn.cursor
            if fiprovider_id:
                update()
            else:
                fiprovider_id = insert()
            return Provider(
                fiprovider_id=fiprovider_id,
                fiprov_status=fiprov_status,
                fdstart_date=fdstart_date,
                fdend_date=fdend_date,
                fsprovider_code=fsprovider_code,
                fsdesc=fsdesc
            )

    @staticmethod
    def dump() -> list:
        """
        :return: list of all providers objects
        """
        with db_conn:
            cursor = db_conn.cursor
            cursor.execute(
                "SELECT "
                    "fiprovider_id,"    # [0]
                    "fiprov_status,"    # [1]
                    "fdstart_date,"     # [2]
                    "fdend_date,"       # [3]
                    "fsprovider_code,"  # [4]
                    "fsdesc "           # [5]
                "FROM mycapp.provider"
            )
            return [Provider(pr[0], pr[1], pr[2], pr[3], pr[4], pr[5]) for pr in cursor.fetchall()]


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
    def get(fsserv_code):
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
                "mycapp.service(fiservice_status, fsserv_code, fsserv_desc) "
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
    def delete(ids_todelete: tuple):
        if not ids_todelete:
            return
        LOG.debug(
            "Try to delete services: {}".format(ids_todelete))
        with db_conn:
            cursor = db_conn.cursor
            n = len(ids_todelete)
            cursor.execute(
                "DELETE FROM mycapp.service WHERE fiservice_id IN ({}{})".format("%s," * (n - 1), "%s"),
                ids_todelete
            )

    @staticmethod
    def dump() -> list:
        """
        :return: List of all services objects
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
