from conversions import *
from core_crypto import *

hashDict = {}
total = 10000000

for i in xrange(1,total):
    hashd = sha1_int(str(i))

    relev = least_50bits = bin(hashd)[-26:]

    #relev = hashd[(len(hashd)-7):]      # 7 bytes, 56 bits
    #mask  = "03ffffffffffff"            # mask to ignore 6 most significant bits
    #relev = xor_strings(relev, hex_to_ascii(mask))

    if relev in hashDict:
        print " *** Collision found ", hashDict[relev], " and ", i
        break
    hashDict[relev] = i

print hashDict[relev], " = "+sha1_hex(str(hashDict[relev]))
print i, " = "+sha1_hex(str(i))
