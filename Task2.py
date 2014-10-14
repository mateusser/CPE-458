from core_crypto import *
import base64

key = "CALIFORNIA LOVE!"

fp = open("Lab2.TaskII.A.txt", "r")
cipherb64 = fp.read()
fp.close()

cipher = base64.b64decode(cipherb64)

paddedPlain = ecb_decrypt(cipher, key)

plain = pkcs7_strip(paddedPlain, AES.block_size)

print paddedPlain
	
