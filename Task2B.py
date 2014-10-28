from conversions import *
from core_crypto import *

hashDict = {}
total = 100000000

for i in xrange(1, total):
    hashd = sha1_int(str(i))

    relev = least_50bits = bin(hashd)[-50:]

    if relev in hashDict:
        print " *** Collision found ", hashDict[relev], " and ", i
        break
    hashDict[relev] = i

print hashDict[relev], " = "+sha1_hex(str(hashDict[relev]))
print i, " = "+sha1_hex(str(i))

# *** Collision found  23612730  and  72349653
#23612730  = 48cf792af65204f61439c92df40eb77a7129a491
#72349653  = 58c955b55efe3cfe3a1b0c7b2a5eb77a7129a491
#										eb77a7129a491 = 52 bits
