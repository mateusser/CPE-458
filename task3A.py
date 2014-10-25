#!/usr/bin/python
# -*- coding: utf-8 -*-

#Authors:
#   Matheus de Sousa Faria    (desousaf at calpoly.edu)
#   Mateus Seehagen Rodrigues (mrodr107 at calpoly.edu)

import requests

from core_crypto import *

SITE_URL = 'http://localhost:8080'
POST_URL = SITE_URL + '/post'
QUERY_URL = SITE_URL + '/?who={}&what={}&mac={}'

query_pattern = 'who={}&what={}&mac={}'

def sha1_padding(message):
    ml = len(message)*8

    message_inbits = ''.join(bin(ord(letter))[2:].rjust(8, '0') for letter in message)
    message_inbits += '1'

    while (len(message_inbits) % 512) != 448:
        message_inbits += '0'
    message_inbits += bin(ml)[2:].rjust(64, '0')

    ascii_message = ''
    for index in range(0, len(message_inbits), 8):
        ascii_message += chr(int(message_inbits[index : index + 8], 2))
    return ascii_message

def sha1_get_next_int_hash(intHash, originalMessage, newMessage):
    mask32 = 0xffffffff

    rotate_left = lambda uint, n: ((uint << n) | (uint >> (32 - n))) & mask32
    mask = lambda uint: uint & mask32

    h0 = mask(intHash >> 128)
    h1 = mask(intHash >> 96)
    h2 = mask(intHash >> 64)
    h3 = mask(intHash >> 32)
    h4 = mask(intHash)

    message = originalMessage + newMessage
    ml = len(message)*8

    message_inbits = ''.join(bin(ord(letter))[2:].rjust(8, '0') for letter in message)
    message_inbits += '1'
    while (len(message_inbits) % 512) != 448:
        message_inbits += '0'
    message_inbits += bin(ml)[2:].rjust(64, '0')

    chunks = []
    for index in range(len(originalMessage)*8,len(message_inbits), 512):
        chunks.append(message_inbits[index : index + 512])

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

def getMessageAndMac():
    url = requests.get(SITE_URL + '/post').url
    url = url.replace('%20', ' ')
    url = url[url.index('?') + 1:]
    fields = url.split('&')
    data = {}
    for field in fields:
        key, value = field.split('=')
        data[key] = value
    return data

def sendMessageAndMac(who, what, mac):
    url = QUERY_URL.format(who, what, mac)
    html = requests.get(url).text

    if 'Invalid signature.' in html:
        return False
    else:
        print 'Message Posted.'
        print
        print html
        print
        print 'SUCCESS! \o/'
        return True



post = getMessageAndMac()
post_query = query_pattern.format(post['who'], post['what'], post['mac'])

print 'Getting a post...'
print post_query
print

what_padded = sha1_padding(post['what'])

print 'Padding the what field...'
print what_padded
print

newMessage = '. New Message...'

print 'New Message Appending...'
print what_padded + newMessage
print

print 'Guessing key size, to correct the pad...'

fake_key = ''
for size in range(512):
    fake_key = 'a'*size
    what_padded_key = sha1_padding(fake_key + post['what'])

    newHash = '%040x' % sha1_get_next_int_hash(int(post['mac'], 16), what_padded_key, newMessage)

    what_padded = what_padded_key[size:]
    if sendMessageAndMac(post['who'], what_padded + newMessage, newHash):
        print
        print query_pattern.format(post['who'], what_padded + newMessage, newHash)
        print 'Key Size: {}'.format(size)
        break
