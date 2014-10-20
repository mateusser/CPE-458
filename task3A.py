#Authors:
#   Matheus de Sousa Faria    (desousaf at calpoly.edu)
#   Mateus Seehagen Rodrigues (mrodr107 at calpoly.edu)

import core_crypto
import conversions

cipher = ''
with open('Lab2.TaskIII.A.txt', 'r') as cipherFile:
    cipher = conversions.b64_to_ascii(cipherFile.read())

key = 'MIND ON MY MONEY'
iv = 'MONEY ON MY MIND'

print core_crypto.cbc_decrypt(cipher, key)
