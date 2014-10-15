from core_crypto import *
from conversions import *
import base64

#####################    TASK A    ####################

key = "CALIFORNIA LOVE!"

fp = open("Lab2.TaskII.A.txt", "r")
cipherb64 = fp.read()
fp.close()

cipher = b64_to_ascii(cipherb64)

plain = ecb_decrypt(cipher, key)

#print plain

#####################    TASK B    ####################

fp = open("Lab2.TaskII.B.txt", "r")
fileContaint = fp.read()
fp.close()

ciphersHEX = fileContaint.split()

ciphers = [0] * len(ciphersHEX)

for i in range(len(ciphersHEX)):
	ciphers[i] = hex_to_ascii(ciphersHEX[i])

	fp = open("./images/image"+str(i)+".bmp", "w")
	fp.write(ciphers[i])
	fp.close()

#plain = ecb_decrypt(cipher, key)

#print plain