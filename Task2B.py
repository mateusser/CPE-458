import hashlib, sys

hashDict = {}  
total = 10000000

for i in xrange(1,total):
    hashd = hashlib.sha1(str(i)).hexdigest()
    relev = hashd[:13]
    relev = relev & 0x3FFFFFFFFFFFF
    if relev in hashDict:
        print " *** Collision found ", hashDict[relev], " and ", i
        sys.exit(0)
    hashDict[relev] = i