import threading
class KTopUrl(object):
    def __init__(self, k):
        self.k = k
        self.kTop = ConstKTop(self.k) # default

    def add_url(self, shorturl):
        self.kTop.add(shorturl)

    def get_topK_urls(self):
        return self.kTop.get_topK()


class ConstKTop(object):
    
    def __init__(self, k):
        self.k = k
        self.top = [str(i) for i in range(self.k + 1)] 
        # adding placeholder in freq table
        self.freq = {str(i):0 for i in range(self.k + 1)} ## placeholder 
        self.lock = threading.Lock()

        #self.freq = {}

    def add(self, key):
        with self.lock:
            # increment the frequency 
            if key in self.freq.keys(): 
                self.freq[key] += 1
            else: 
                self.freq[key] = 1

            # store and adjust top vector
            self.top[self.k] = key

            i = self.top.index(key) 
            i -= 1
            while i >= 0: 

                if (self.freq[self.top[i]] <= self.freq[self.top[i + 1]]): 
                    t = self.top[i] 
                    self.top[i] = self.top[i + 1] 
                    self.top[i + 1] = t 

                else: 
                    break
                i -= 1

    def get_topK(self):
        l = []
        with self.lock:
            i = 0
            l = []
            while i < self.k and len(self.top[i]) > 1: 
                l.append((self.freq[self.top[i]] , self.top[i]))
                i += 1
            # print(l)
            # print(self.freq)
            # print("\n\n")
        return l