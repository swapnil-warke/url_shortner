import abc
from threading import Thread
from threading import Condition
from url_shortner.urldb import keyUtils
from threading import Condition
import time
import sqlobject
from sqlobject.sqlite import sqliteconnection
from threading import current_thread

BLOCK_SIZE = 5
class KeyGenerator(object):
    def __init__(self, generator):
        self.generator = generator

  
    def setGenerator(self, generator):
        self.generator = generator

    def getKeys(self, keydb_connection, no_of_keys):
        return self.generator.getKeys(no_of_keys)


class SQLKeys(object):
    def getKeys(self, no_of_keys):
        return keyUtils.getKeys(no_of_keys)



class KeyCache:
    def __init__(self, capacity):
        self.buffer_capacity = capacity
        self.buffer_size = 0
        self.cv = Condition()
        self.q = []
        self.producer_block_size = BLOCK_SIZE


    def getKey(self):

        self.cv.acquire()
        while self.buffer_size == 0:
            self.cv.wait()

        item = self.q.pop(0)
        self.buffer_size -= 1

        self.cv.notifyAll()
        self.cv.release()


        return item

    # insert multiple string equal to 
    def putKeys(self, items):

        self.cv.acquire()
        while self.buffer_size >= self.buffer_capacity - self.producer_block_size:
            self.cv.wait()

        self.q += items
        self.buffer_size += len(items)
        self.cv.notifyAll()
        self.cv.release()

def GeneratorThread(keycache):
    key_gen = KeyGenerator(SQLKeys())
    while True:
        items = key_gen.getKeys(keydb_connection, BLOCK_SIZE)
        print('\nProduced {0} items'.format(len(items)))
        keycache.putKeys(items)
