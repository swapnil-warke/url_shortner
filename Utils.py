import hashlib

def selectBucket(key:str, bucket_size)->int:
    keyb = str.encode(key)
    return int(hashlib.sha1(keyb).hexdigest(), 16)%bucket_size