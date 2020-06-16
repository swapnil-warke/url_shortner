import sqlobject

class UrlMapping(sqlobject.SQLObject):
    shortUrl = sqlobject.StringCol(length=8, unique=True)
    originalUrl     = sqlobject.StringCol()
    ctime    = sqlobject.IntCol(default=None)
    shortUrl_index      = sqlobject.DatabaseIndex(shortUrl)
    ctime_index  = sqlobject.DatabaseIndex(ctime)