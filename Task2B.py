from conversions import *
from core_crypto import *

hashDict = {}
total = 10000000

for i in xrange(1,total):
    hashd = sha1_int(str(i))

    relev = least_50bits = bin(hashd)[-50:]

    if relev in hashDict:
        print " *** Collision found ", hashDict[relev], " and ", i
        break
    hashDict[relev] = i

print hashDict[relev], " = "+sha1_hex(str(hashDict[relev]))
print i, " = "+sha1_hex(str(i))
