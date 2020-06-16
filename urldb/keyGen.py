import string
import random
import time
import threading
import sqlobject
from sqlobject.sqlite import sqliteconnection
from url_shortner import Params 
from url_shortner.urldb import keyUtils
from url_shortner import Errors


genkey_per_thread = 10
number_of_threads = 8
def threadFunc():
    con = sqlobject.sqlhub.processConnection.getConnection()
    keys_failed = 0
    for i in range(genkey_per_thread):
        shorturl = keyUtils.generate_random_key()
 
        try:
            keyUtils.AddKey(shorturl)
        except Exception as e:
                keys_failed+=1


    print("Inserted %d keys .."%    (genkey_per_thread-keys_failed))


def generate_key_for_db():
    keyUtils.connectToDatabaseAndCreateTables()
    threads = []
    for i in range(number_of_threads):
        threads.append(threading.Thread(target=threadFunc))

    for i in range(number_of_threads):
        threads[i].start()

    for i in range(number_of_threads):
        threads[i].join()

generate_key_for_db()
#rows = keyUtils.getKeys()