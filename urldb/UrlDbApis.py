import time
import sqlobject
from url_shortner.urldb.UrlDbTables import UrlMapping
from url_shortner import Params 
from url_shortner import Errors

def AddUrl(shortUrl, originalUrl):
	try:
		new_url = UrlMapping(shortUrl=shortUrl, originalUrl=originalUrl, ctime=time.time())
		return new_url
	except Exception as e:
		raise 

def getUrlById(id):
	return UrlMapping.get(id)

def createUrlMappingTable():
    UrlMapping.createTable(ifNotExists=True)

def getUrl(shortUrl):
	res = list(UrlMapping.select(UrlMapping.q.shortUrl == shortUrl))
	#print(res)
	if res:
		res = res[0]
	else:
		raise Errors.USError(Errors.URLNOTPRESENT)
	return res

def compactUrl():
	expired_timestamp = time.time() - Params.EXPIRY_PERIOD_URL;
	UrlMapping.deleteMany(UrlMapping.q.ctime < expired_timestamp)



#list(UrlMapping.select(UrlMapping.q.shortUrl == '12345678'))
#list(UrlMapping.select(UrlMapping.q.shortUrl == '1234567s'))
