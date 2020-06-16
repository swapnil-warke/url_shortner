from url_shortner.cache import KeyCache as kc
import abc
from threading import Thread
from threading import Condition
from url_shortner.urldb import keyUtils
from threading import Condition
import time
import sqlobject
from sqlobject.sqlite import sqliteconnection
from threading import current_thread


def consumer_thread(keycache):
    while True:
        item = keycache.getKey()
        print("\n{0} consumed item {1}".format(current_thread().getName(), item), flush=True)
        time.sleep(.5)

if __name__ == "__main__":
    #con = sqliteconnection.SQLiteConnection('/d/Users/swapnilw/Document/codes/pycodes/url_shortner/urldb/key_db.db', driver='sqlite3')
    con = sqliteconnection.SQLiteConnection('key_db.db', driver='sqlite3')
    sqlobject.sqlhub.processConnection = con 
    keycache = kc.KeyCache(20)

    consumerThread1 = Thread(target=consumer_thread, name="consumer-1", args=(keycache,), daemon=True)
    consumerThread2 = Thread(target=consumer_thread, name="consumer-2", args=(keycache,), daemon=True)
    producerThread1 = Thread(target=kc.GeneratorThread, name="producer-1", args=(keycache,), daemon=True)
    producerThread2 = Thread(target=kc.GeneratorThread, name="producer-2", args=(keycache,), daemon=True)

    consumerThread1.start()
    consumerThread2.start()
    producerThread1.start()
    producerThread2.start()
    print("Threads started")
    time.sleep(1000)
    print("Main thread exiting")