
from collections import OrderedDict 
import threading


class SimpleLRU(object): 
    
    # initialising capacity 
    def __init__(self, capacity: int): 
        self.cache = OrderedDict() 
        self.capacity = capacity 

    def get(self, key: str) -> {}: 
        if key not in self.cache: 
            raise KeyError
        else: 
            self.cache.move_to_end(key) 
            return self.cache[key] 

    def put(self, key: str, value: {}) -> None:   
        self.cache[key] = value 
        self.cache.move_to_end(key) 
        if len(self.cache) > self.capacity: 
            self.cache.popitem(last = False) 

    def invalidate(self,key: str):
        try:
            del self.cache[key]
        except Exception as e:
            pass # We are expecting Key error if key is not present


class LRUCache(object):
    def __init__(self, capacity: int):
        self.cache_lock = threading.Lock()
        self.simple_lru = SimpleLRU(capacity)

    def get(self, key: str) -> {}: 
        value = {}
        with self.cache_lock:
            value = self.simple_lru.get(key)
        return value

    def put(self, key: str, value: {}) -> None:   
        with self.cache_lock:
            self.simple_lru.put(key, value)


    def invalidate(self,key: str):
        with self.cache_lock:
            self.simple_lru.invalidate(key)







