import hashlib, sys
from conversions import *
from core_crypto import *

hashDict = {}  
total = 10000000

for i in xrange(1,total):
    hashd = hashlib.sha1(str(i)).hexdigest()
    relev = hashd[(len(hashd)-7):]		# 7 bytes, 56 bits
    mask  = "03ffffffffffff"			# mask to ignore 6 most significant bits
    relev = xor_strings(relev, hex_to_ascii(mask))
    if relev in hashDict:
        print " *** Collision found ", hashDict[relev], " and ", i
        break
    hashDict[relev] = i

print hashDict[relev], " = "+hashlib.sha1(str(hashDict[relev])).hexdigest()
print i, " = "+hashlib.sha1(str(i)).hexdigest()