import hashlib

sign  = hashlib.md5()
content = 'i am a handsom man'.encode('utf-8')
sign.update(content)
print(sign.hexdigest())
