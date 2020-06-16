import json
import cherrypy
import sys
import time
import sqlobject
from sqlobject.sqlite import sqliteconnection
from url_shortner.urldb import UrlDbApis
from url_shortner import Errors
from url_shortner import Params
from url_shortner.cache import KeyCache as kc
from url_shortner.cache import LRUCache as lruc
from url_shortner.cache import kTopUrl as ktop
import threading
import builtins
from url_shortner.urldb import keyUtils
from url_shortner import Utils


def compacturl_threadfunc():
    while True:
        time.sleep(12*60*60)
        UrlDbApis.compactUrl()
    
def only_post():
    if cherrypy.request.method.upper() not in ['HEAD', 'POST']:
        raise cherrypy.HTTPError(405)
cherrypy.tools.only_post = cherrypy.Tool('on_start_resource', only_post)

def error_response( status, message, traceback, version):
    cherrypy.response.headers['Content-Type'] = 'application/json'
    return json.dumps({
                'code': status,
                'message': message,
                'retryable': False,
                'data': {}
        })

def handle_error():
    print('Some Error occurred handle_error')
    exception = sys.exc_info()[1]
    error_codes ={

    }
    if isinstance(exception, cherrypy.HTTPRedirect):
        raise exception
    if isinstance(exception, cherrypy.HTTPError):
        code = exception.code
        msg = exception.message
        http_code = cherrypy.response.getcode()
    else:
        code = -1
        msg = 'Internal Error'
        http_code = 500
        if isinstance(exception, Errors.USError):
            code = exception.us_errno
            msg = exception.us_errmsg
            if exception.is_http_error:
                http_code = exception.http_code


    cherrypy.response.status = http_code
    error_response = {
            'code': http_code,
            'message': msg+"...",
            'retryable': False,
            'data': {}
    }
    cherrypy.response.body = json.dumps(error_response).encode('utf-8')

class HelloWorldApp(object):
    @cherrypy.expose()
    def index(self):
        print('index request Handler@@@')
        return '''<html>
        <body>Hello World from Swapnil</body>
        </html>
        '''

class UrlShortner(object):
    @cherrypy.expose('add_url')
    @cherrypy.tools.only_post()
    def addURL(self, originalUrl):
        ## approach 1
            # get url from memory here also create buckets to hold cache
            # randomly assign bucket
            # get key from bucket and insert into db
            # if bucket is empty get keys from db
        ## approach 2
            # have multiple bucket counter
            # get shortUrl = md5(bucket_id+bucket_counter+originalUrl) mod 8 chars
        retries = 3
        while retries >  0:
            try:
                shortUrl = keycache.getKey()
                UrlDbApis.AddUrl(shortUrl, originalUrl)
                break
            except Exception as e:
                retries-=1
                if retries <= 0:
                    print("Error occurred in addURL: %s"%str(e))
                    raise
        return json.dumps({
            "code"  : 200,
            "msg"   : "User http://localhost:8090/getURL?shortUrl={0} for {1}".format(shortUrl, originalUrl),    
            })


    @cherrypy.expose('get_url')
    @cherrypy.tools.only_post()
    def getURL(self, shortUrl):
        print("Request for {0} received".format(shortUrl))
        try:
            # key to look in cache is salt(url+salt) % number_of_cache_buckets
            # Try to get url from cache
            # if not present in cache get it from db
            # set in cache
            # redirect
            pick = Utils.selectBucket(shortUrl, Params.NO_OF_BUCKETS)
            #print("### Bucket {0}".format(str(pick)))
            pick_cache = cache_buckets[pick]
            originalUrl = ''
            try:
                pick_cache[1].add_url(shortUrl) ## topk cache
                urlobj=pick_cache[0].get(shortUrl) # cache
                originalUrl = urlobj['originalUrl']
                #print("Got {0} from cache".format(urlobj))
            except KeyError:
                urlobj = UrlDbApis.getUrl(shortUrl)
                #print("Got {0} from db".format(urlobj))
                originalUrl = urlobj.originalUrl
                pick_cache[0].put(shortUrl, {'originalUrl':originalUrl})
            except Exception as e:
                print("Error occurred in getURL {0}".fromat(str(e)))
                raise

            raise cherrypy.HTTPRedirect(originalUrl)
        except Exception as e:
            if isinstance(e, cherrypy.HTTPRedirect):
                print("Redirecting {0} to {1}  ...".format(shortUrl, originalUrl))
            else:
                print("Error occurred %s", str(e))
            raise

    @cherrypy.expose('get_top')
    def getTop(self):
        try:
            result = []
            for  i in range(Params.NO_OF_BUCKETS):
                result+=(cache_buckets[i][1].get_topK_urls())
            
            # simple sorting logic for merge result of different buckets
            result.sort(reverse=True)
            result = result[:Params.TOPK]
            
            #print("Result of getTop : {0}".format(str(result)))
            response = {"TopK Urls : {0}".format(str(result))}
            return response
        except Exception as e:
            print("getTop Error:  {0}".format(str(e)))
            raise

        

def connectToDatabaseAndCreateTables():
        con = sqliteconnection.SQLiteConnection(Params.SQLLITE_DB_PATH, driver='sqlite3')
        __builtins__.urldb_connection = con
        sqlobject.sqlhub.processConnection = con 
        UrlDbApis.createUrlMappingTable()
        con = sqliteconnection.SQLiteConnection(Params.SQLLITE_KEYDB_PATH, driver='sqlite3')
        __builtins__.keydb_connection = con
        keyUtils.createKeysTable()

def startServer(port, app):
    if cherrypy.engine.state == cherrypy.engine.states.STARTED:
        cherrypy.engine.stop()
        
    server_confg = {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': port,
        'server.thread_pool': 8, # params.server_threads
        'server.socket_queue_size': 16,
        'server.socket_timeout': 30,
        'engine.autoreload_on': False,
        'response.header_server': 'Webserver',
        'tools.session.httponly': True,

    }
    api_config = {
        '/': {
            'request.error_response': handle_error,
            'error_page.default'    : error_response
            }
        }
    
    #cherrypy.tree.mount(api_root, '/')
    cherrypy.config.update(server_confg)
    cherrypy.tree.mount(app, '/', api_config)
    cherrypy.tree.mount(HelloWorldApp(), '/test')
    
    cherrypy.engine.start()
    
    
    #cherrypy.engine.block()
    #cherrypy.quickstart(app)

if __name__ == '__main__':
    try:
        connectToDatabaseAndCreateTables()

        kctemp = kc.KeyCache(Params.KEYDB_CACHE_SIZE)
        __builtins__.keycache = kctemp
        th = threading.Thread(target=kc.GeneratorThread, name="Key Generation Thread", 
                        args=(keycache,))
        __builtins__.keygen_thread = th
        keygen_thread.start()

        th = threading.Thread(target=compacturl_threadfunc, name="Expired UrlCompaction Thread")
        __builtins__.compaction_thread = th
        compaction_thread.start()

        cache_buckets = []
        for  i in range(Params.NO_OF_BUCKETS):
            cache_buckets.append((lruc.LRUCache(Params.CACHE_SIZE_PER_BUCKETS), ktop.KTopUrl(Params.TOPK)))
        __builtins__.cache_buckets = cache_buckets


    
        #cherrypy.config.update({'server.socket_port': 8091})
        startServer(8090, UrlShortner())
        print("Server started. .. ...")

    except Exception as e:
        print(str(e))