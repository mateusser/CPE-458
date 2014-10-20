#Authors:
#   Matheus de Sousa Faria    (desousaf at calpoly.edu)
#   Mateus Seehagen Rodrigues (mrodr107 at calpoly.edu)

from Crypto.Cipher import AES
from conversions import *

def pkcs7_pad(plain,blocksize):
    padbyte = blocksize - len(plain)%blocksize
    for i in range(padbyte):
        plain += chr(padbyte)
    return plain


def pkcs7_strip(plain,blocksize):
    numblocks = len(plain)/(blocksize) + (1 if len(plain)%blocksize else 0)

    newplain = plain[0:(numblocks-1)*blocksize]
    padblock = plain[(numblocks-1)*blocksize:]
    padbytes = int(padblock[-1:].encode("hex"),16)
    #Validate padding - we should never see a pad end in zero
    if padbytes == 0:
        raise Exception("PaddingError")
    #make sure all the pad bytes make sense
    for i in range(padbytes-1):
        if padblock[-padbytes+i:-padbytes+i+1] != chr(padbytes):
            raise Exception("PaddingError")
    newplain += padblock[:-padbytes]

    return newplain

if __name__ == "__main__":
    print 'Pad "My Message"'
    padded = pkcs7_pad('My Message', 16)
    print padded
    print ascii_to_hex(padded)
    print 'Unpad'
    unpadded = pkcs7_strip(padded, 16)
    print unpadded
    print
    print
    print 'Block with size sixteen'
    padded = pkcs7_pad('a'*16, 16)
    print padded
    print ascii_to_hex(padded)
    print 'Unpad'
    unpadded = pkcs7_strip(padded, 16)
    print unpadded
