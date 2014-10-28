#!/usr/bin/python
# -*- coding: utf-8 -*-

#Authors:
#   Matheus de Sousa Faria    (desousaf at calpoly.edu)
#   Mateus Seehagen Rodrigues (mrodr107 at calpoly.edu)

from Crypto.Cipher import AES

def otp_encrypt(pt,key):
    ct = ""
    if(len(pt) > len(key)):
        raise Exception("KeyLengthError")
        return ct

    for i in range(len(pt)):
        ct += chr(ord(pt[i:i+1]) ^ ord(key[i:i+1]))
    return ct


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


#C_i = E_k(M_i xor C_(i-1)), C_0 = IV
#plain, iv, and key all expected to be of size BLOCKSIZE
def cbc_encrypt(plain, iv, key):
    aes_obj = AES.new(bytes(key))
    BLOCKSIZE = AES.block_size

    plain = pkcs7_pad(plain,BLOCKSIZE)

    numcipherblocks = len(plain)/(BLOCKSIZE) + (1 if len(plain)%BLOCKSIZE else 0)

    cipher = ""
    c_imin1 = iv
    for i in range(numcipherblocks):
        m_xor_c = ""
        m_i = plain[i*BLOCKSIZE: i*BLOCKSIZE + BLOCKSIZE]
        #M_i xor C_(i-1))
        for j in range(BLOCKSIZE):
            m_xor_c += chr(ord(m_i[j:j+1]) ^ ord(c_imin1[j:j+1]))
        #E_k(M_i xor C_(i-1)),
        c_imin1 = aes_obj.encrypt(m_xor_c)
        cipher += c_imin1
    cipher = iv + cipher
    return cipher


#M_i = D_k(C_i) xor C_(i-1)
def cbc_decrypt(cipher, key):
    aes_obj = AES.new(bytes(key))
    BLOCKSIZE = AES.block_size

    iv = cipher[:BLOCKSIZE]

    cipher = cipher[BLOCKSIZE:]

    numplainblocks = len(cipher)/BLOCKSIZE

    plain = ""
    c_imin1 = iv #grab the IV
    for i in range(numplainblocks):
        c_i = cipher[i*BLOCKSIZE:i*BLOCKSIZE + BLOCKSIZE]
        #D_k(C_i)
        m_xor_c = aes_obj.decrypt(c_i)
        #D_k(C_i) xor C_(i-1)
        for j in range(BLOCKSIZE):
            plain += chr(ord(m_xor_c[j:j+1]) ^ ord(c_imin1[j:j+1]))
        c_imin1 = cipher[i*BLOCKSIZE:i*BLOCKSIZE + BLOCKSIZE]

    plain = pkcs7_strip(plain, BLOCKSIZE)

    return plain


def ecb_encrypt(plain,key):
    aes_obj = AES.new(bytes(key))
    BLOCKSIZE = AES.block_size

    plain = pkcs7_pad(plain,BLOCKSIZE)

    numcipherblocks = len(plain)/(BLOCKSIZE) + (1 if len(plain)%BLOCKSIZE else 0)

    cipher = ""
    for i in range(numcipherblocks):
        m_i = plain[i*BLOCKSIZE: i*BLOCKSIZE + BLOCKSIZE]
        #E_k(M_i),
        cipher += aes_obj.encrypt(m_i)
    return cipher


def ecb_decrypt(cipher,key):
    aes_obj = AES.new(bytes(key))
    BLOCKSIZE = AES.block_size

    numcipherblocks = len(cipher)/(BLOCKSIZE) + (1 if len(cipher)%BLOCKSIZE else 0)

    plain = ""
    for i in range(numcipherblocks):
        m_i = cipher[i*BLOCKSIZE: i*BLOCKSIZE + BLOCKSIZE]
        #E_k(M_i),
        plain += aes_obj.decrypt(m_i)

    plain = pkcs7_strip(plain,BLOCKSIZE)

    return plain


def print_message_in_blocks(message, block_size):
    blocks = get_message_in_blocks(message, block_size)
    for block in blocks:
        print '[{}]'.format(block)


def get_message_in_blocks(message, block_size):
    blocks = []
    n_blocks = len(message)/block_size
    if len(message) % block_size:
        n_blocks += 1
    for i in range(n_blocks):
        blocks.append(message[block_size*i : block_size*(i + 1)])
    return blocks

def xor_strings(plaintext, key):
    pt_len = len(plaintext)
    k_len = len(key)
    if k_len < pt_len:
        key = key*(pt_len / k_len) + key[:(pt_len % k_len)]
    elif k_len > pt_len:
        key = key[:pt_len]

    xor = ''
    for k, c in zip(key, plaintext):
        xor += '{}'.format(chr(ord(k) ^ ord(c)))

    return xor


def sha1_int(message):
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
    return hh

def sha1_hex(message):
    digest = '%040x' % (sha1_int(message))
    return digest
