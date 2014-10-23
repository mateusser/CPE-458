#!/usr/bin/python
# -*- coding: utf-8 -*-


def sha1(message):
    #Note 1: All variables are unsigned 32 bits and wrap modulo 232 when calculating, except
    #        ml the message length which is 64 bits, and
    #        hh the message digest which is 160 bits.
    #Note 2: All constants in this pseudo code are in big endian.
    #        Within each word, the most significant byte is stored in the leftmost byte position
    #
    #Initialize variables:
    #
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0
    #
    #ml = message length in bits (always a multiple of the number of bits in a character).
    #
    ml = len(message)*8
    message_inbits = ''.join(bin(ord(letter))[2:].rjust(8, '0') for letter in message)

    #Pre-processing:
    #append the bit '1' to the message i.e. by adding 0x80 if characters are 8 bits. 
    #append 0 ≤ k < 512 bits '0', thus the resulting message length (in bits)
    #   is congruent to 448 (mod 512)
    #append ml, in a 64-bit big-endian integer. So now the message length is a multiple of 512 bits.
    #
    print ml + 1
    print (ml + 1) % 448
    print 448 - ((ml + 1) % 448)
    print ml + 1 + (448 - ((ml + 1) % 448))
    message_inbits += '1' + '0'*(448 - ((ml + 1) % 448)) + bin(ml)[2:].rjust(64, '0')
    print message_inbits
    print len(message_inbits)

    #Process the message in successive 512-bit chunks:
    #break message into 512-bit chunks
    chunks = []
    for index in range(len(message_inbits)/512):
        chunks.append(message_inbits[index*512 : index*512 + 512])
    print chunks

    #for each chunk
    #    break chunk into sixteen 32-bit big-endian words w[i], 0 ≤ i ≤ 15
    #
    mask = 0xffffffff
    for chunk in chunks:
        w = []
        for index in range(len(chunk)/32):
            w.append(int(message_inbits[index*32 : index*32 + 32], 2) & mask)

    #    Extend the sixteen 32-bit words into eighty 32-bit words:
    #    for i from 16 to 79
    #        w[i] = (w[i-3] xor w[i-8] xor w[i-14] xor w[i-16]) leftrotate 1
    #
        for i in range(16, 80):
            w.append(((w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16]) << 1) & mask)

    #    Initialize hash value for this chunk:
    #    a = h0
    #    b = h1
    #    c = h2
    #    d = h3
    #    e = h4
    #
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4

        unot = lambda uint: int(bin(~b)[4:], 2) & mask
    #    Main loop:[42]
    #    for i from 0 to 79
        for i in range(80):
    #        if 0 ≤ i ≤ 19 then
    #            f = (b and c) or ((not b) and d)
    #            k = 0x5A827999
            if 0 <= i and i <= 19:
                f = (b & c) | (unot(b) & d)
                k = 0x5A827999
    #        else if 20 ≤ i ≤ 39
    #            f = b xor c xor d
    #            k = 0x6ED9EBA1
            elif 20 <= i and i <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
    #        else if 40 ≤ i ≤ 59
    #            f = (b and c) or (b and d) or (c and d) 
    #            k = 0x8F1BBCDC
            elif 40 <= i and i <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
    #        else if 60 ≤ i ≤ 79
    #            f = b xor c xor d
    #            k = 0xCA62C1D6
            elif 60 <= i and i <= 79:
                f = b ^ c ^ d
                k = 0xCA62C1D6
    #
    #        temp = (a leftrotate 5) + f + e + k + w[i]
    #        e = d
    #        d = c
    #        c = b leftrotate 30
    #        b = a
    #        a = temp
    #
            f = f & mask
            temp = ((a << 5) + f + e + k + w[i]) & mask
            e = d & mask
            d = c & mask
            c = (b << 30) & mask
            b = a & mask
            a = temp
    #    Add this chunk's hash to result so far:
    #    h0 = h0 + a
    #    h1 = h1 + b 
    #    h2 = h2 + c
    #    h3 = h3 + d
    #    h4 = h4 + e
    #
        h0 = (h0 + a) & mask
        h1 = (h1 + b) & mask
        h2 = (h2 + c) & mask
        h3 = (h3 + d) & mask
        h4 = (h4 + e) & mask

    #Produce the final hash value (big-endian) as a 160 bit number:
    #hh = (h0 leftshift 128) or (h1 leftshift 96) or (h2 leftshift 64) or (h3 leftshift 32) or h4
    hh = (h0 << 128) | (h1 << 96) | (h2 << 64) | (h3 << 32) | h4
    return hh


if __name__ == '__main__':
    print hex(sha1('abc'))
    print
    print hex(sha1('abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq'))
