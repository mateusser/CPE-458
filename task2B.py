from core_crypto import *
from conversions import *

def isECB(cipher):
    blocks = []
    for i in range(len(cipher)/AES.block_size):
        blocks.append(cipher[i*AES.block_size:i*AES.block_size + AES.block_size])

    for block in blocks:
        if blocks.count(block) > 1:
            return True
    return False

with open("Lab2.TaskII.B.txt", "r") as fp:
    fileContaint = fp.read()

ciphersHEX = fileContaint.split()

for i in range(len(ciphersHEX)):
    cipher  = hex_to_ascii(ciphersHEX[i])

    if isECB(cipher):
        with open("./images/image"+str(i)+".bmp", "w") as fp:
            fp.write(cipher)
