import time
import sqlobject
from sqlobject.sqlite import sqliteconnection



class UrlMapping(sqlobject.SQLObject):
    shortUrl = sqlobject.StringCol(length=8, unique=True)
    originalUrl     = sqlobject.StringCol()
    ctime    = sqlobject.IntCol(default=None)
    shortUrl_index      = sqlobject.DatabaseIndex(shortUrl)
    ctime_index  = sqlobject.DatabaseIndex(ctime)


def createTable():
    UrlMapping.createTable(ifNotExists=True)


def init_sqlite_db():
    con = sqliteconnection.SQLiteConnection('urldb/url_db.db', driver='sqlite3')
    sqlobject.sqlhub.processConnection= con
    createTable()
    con.close()

init_sqlite_db()
