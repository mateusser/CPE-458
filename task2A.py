#Authors:
#   Matheus de Sousa Faria    (desousaf at calpoly.edu)
#   Mateus Seehagen Rodrigues (mrodr107 at calpoly.edu)

from core_crypto import *
from conversions import *

key = "CALIFORNIA LOVE!"

with open("Lab2.TaskII.A.txt", "r") as fp:
    cipherb64 = fp.read()

cipher = b64_to_ascii(cipherb64)
plain = ecb_decrypt(cipher, key)

print plain
