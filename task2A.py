#Authors:
#   Matheus de Sousa Faria    (desousaf at calpoly.edu)
#   Mateus Seehagen Rodrigues (mrodr107 at calpoly.edu)

#!/usr/bin/python
# -*- coding: utf-8 -*-

def sha1(message):
    mask32 = 0xffffffff

    rotate_left = lambda uint, n: ((uint << n) | (uint >> (32 - n))) & mask32
    mask = lambda uint: uint & mask32

    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0

    ml = len(message)*8

    message_inbits = ''.join(bin(ord(letter))[2:].rjust(8, '0') for letter in message)
    message_inbits += '1'
    while (len(message_inbits) % 512) != 448:
        message_inbits += '0'
    message_inbits += bin(ml)[2:].rjust(64, '0')

    chunks = []
    for index in range(len(message_inbits)/512):
        chunks.append(message_inbits[index*512 : index*512 + 512])

    for chunk in chunks:
        w = []
        for index in range(len(chunk)/32):
            w.append(int(chunk[index*32 : index*32 + 32], 2))

        for i in range(16, 80):
            w.append(rotate_left(w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16], 1))

        a = h0
        b = h1
        c = h2
        d = h3
        e = h4

        for i in range(80):
            if 0 <= i and i <= 19:
                f = d ^ (b & (c ^ d))
                k = 0x5A827999
            elif 20 <= i and i <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= i and i <= 59:
                f = (b & c) ^ (b & d) ^ (c & d)
                k = 0x8F1BBCDC
            elif 60 <= i and i <= 79:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            temp = (rotate_left(a,  5) + mask(f) + e + k + w[i]) % 2**32
            e = mask(d)
            d = mask(c)
            c = rotate_left(b, 30)
            b = mask(a)
            a = temp

        h0 = (h0 + a) % (2**32)
        h1 = (h1 + b) % (2**32)
        h2 = (h2 + c) % (2**32)
        h3 = (h3 + d) % (2**32)
        h4 = (h4 + e) % (2**32)

    hh = (h0 << 128) | (h1 << 96) | (h2 << 64) | (h3 << 32) | h4
    return '%08x' % (hh)


if __name__ == '__main__':
    test_vector = {
        'abc': 'a9993e364706816aba3e25717850c26c9cd0d89d',
        '': 'da39a3ee5e6b4b0d3255bfef95601890afd80709',
        'abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq': '84983e441c3bd26ebaae4aa1f95129e5e54670f1',
        'abcdefghbcdefghicdefghijdefghijkefghijklfghijklmghijklmnhijklmnoijklmnopjklmnopqklmnopqrlmnopqrsmnopqrstnopqrstu': 'a49b2446a02c645bf419f995b67091253a04a259',
    }
    for test in test_vector:
        print 'Message:  {}'.format(test)
        print 'Expected: {}'.format(test_vector[test])
        print 'Received: {}'.format(sha1(test))
        if test_vector[test] != sha1(test):
            print 'Test case Failed'
        else:
            print 'Test case Succed'
        print
        print
