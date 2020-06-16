URLNOTPRESENT = 2001
KEYDBEXAUSTED = 2002
URLNOTAVAILABLE = 2003


# msg key compulsory
# http_code is optional
ERROR_MAP = {}
ERROR_MAP[URLNOTPRESENT] = {"msg": "Url not present for this entry", 'http_code':405}
ERROR_MAP[KEYDBEXAUSTED] = {"msg": "Generate new keys"}
ERROR_MAP[URLNOTAVAILABLE] = {"msg": "Url not available"}


class USError(Exception):
    def __init__(self, errno, msg=''):
        self.us_errno = errno
        self.us_errmsg = msg
        if msg is '':
                self.us_errmsg = ERROR_MAP[errno]['msg']

        self.is_http_error = False        
        self.http_code = 500
        
        if errno in ERROR_MAP and 'http_code' in ERROR_MAP[errno]:
            self.is_http_error = True
            self.http_code = ERROR_MAP[errno]['http_code']
            
