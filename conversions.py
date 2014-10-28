#Authors:
#   Matheus de Sousa Faria    (desousaf at calpoly.edu)
#   Mateus Seehagen Rodrigues (mrodr107 at calpoly.edu)

import binascii
import base64

def ascii_to_hex(string):
    return string.encode('hex')


def hex_to_ascii(hexstring):
    return hexstring.decode('hex')


def b64_to_hex(b64string):
    return binascii.a2b_base64(b64string).encode('hex').strip()


def hex_to_b64(hexstring):
    return binascii.b2a_base64(hexstring.decode('hex')).strip()


def b64_to_ascii(b64string):
    return base64.b64decode(b64string)


def ascii_to_b64(string):
    return base64.b64encode(string)

if __name__ == "__main__":
    print '{} ascii in hex: {}'.format('ab', ascii_to_hex('ab'))
    print '{} hex in ascii: {}'.format(
        ascii_to_hex('ab'),
        hex_to_ascii(ascii_to_hex('ab'))
    )
    print '{} hex in base 64: {}'.format('fa', hex_to_b64('fa'))
    print '{} base 64 in hex: {}'.format(
        hex_to_b64('fa'),
        b64_to_hex(hex_to_b64('fa'))
    )
