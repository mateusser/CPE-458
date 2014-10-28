import hashlib
from conversions import *
from core_crypto import *

#function hmac (key, message)
#    if (length(key) > blocksize) then
#        key = hash(key) // keys longer than blocksize are shortened
#    end if
#    if (length(key) < blocksize) then
#        key = key | [0x00 * (blocksize - length(key))] // keys shorter than blocksize are zero-padded (where | is concatenation)
#    end if
#   
#    o_key_pad = [0x5c * blocksize] XOR key // Where blocksize is that of the underlying hash function
#    i_key_pad = [0x36 * blocksize] XOR key 
#   
#    return hash(o_key_pad | hash(i_key_pad | message)) // Where | is concatenation
#end function

def hmac_sha1(key, message):
	blocksize = 64	# 64 bytes for SHA-1 * 2 for hex

	if(len(key) > blocksize):
		key = hex_to_ascii(hashlib.sha1(key).hexdigest())

	if(len(key) < blocksize):
		key = key + chr(0)*(blocksize-len(key))

	o_key_pad = xor_strings(chr(92) * blocksize, key)
	i_key_pad = xor_strings(chr(54) * blocksize, key)

	hash1 = hex_to_ascii(hashlib.sha1(i_key_pad+message).hexdigest())
	#print "\n\nopad: "+ascii_to_hex(o_key_pad)
	hash2hex = hashlib.sha1(o_key_pad+hash1).hexdigest()

	return hash2hex

key = "000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f"
message = "Sample #1"

print "key: "+key
print "\n\nmessage: "+message
																		   
hmac_sha1(hex_to_ascii(key), "Sample #1")

