import hashlib

sign  = hashlib.md5()
content = 'handsomman'.encode('utf-8')
sign.update(content)
print(sign.hexdigest())
