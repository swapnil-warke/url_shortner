import string
import random
import time
import threading
import sqlobject
from sqlobject.sqlite import sqliteconnection
from url_shortner import Params
import builtins


class Keys(sqlobject.SQLObject):
    shortUrl = sqlobject.StringCol(length=8, unique=True)

def AddKey(shortUrl):
    return Keys(shortUrl=shortUrl)

def createKeysTable():
    Keys.createTable(ifNotExists=True)

def getMinKey():
    res = selectKeys(1)
    return res[0].id


def selectKeys(nrows=5):
    query = Keys.select(connection=keydb_connection)
    res = list(query[:nrows])
    if res:
        return res
    else:
        raise Errors.USError(Errors.KEYDBEXAUSTED)

def selectKeysId(id, nrows=5):
    query = Keys.select(Keys.q.id >= id)    
    res = list(query[:nrows])
    if res:
        return res
    else:
        raise Errors.USError(Errors.KEYDBEXAUSTED)

def deleteKeysId(id, nrows=5):
    Keys.deleteMany(Keys.q.id >= id and Keys.q.id < id+n)

def getKeysId(id, nrows=5):
    rows = selectKeysId(id, nrows)
    ret = []
    for row in rows:
        ret.append(row.shortUrl)
        row.destroySelf()
    return ret    

def getKeys(nrows=5):
    rows = selectKeys(nrows)
    ret = []
    for row in rows:
        ret.append(row.shortUrl)
        row.destroySelf()
    return ret    

KEY_LEN = 8
def generate_random_key():
    # printing letters
    letters = string.ascii_letters + string.digits
    #letters+="._"
    return ''.join(random.choice(letters) for i in range(KEY_LEN))

def connectToDatabaseAndCreateTables():
    con = sqliteconnection.SQLiteConnection(Params.KEYDBNAME, driver='sqlite3')
    sqlobject.sqlhub.processConnection = con 
    createKeysTable()
