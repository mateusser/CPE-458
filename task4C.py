#!/usr/bin/python
# -*- coding: utf-8 -*-

#Authors:
#   Matheus de Sousa Faria    (desousaf at calpoly.edu)
#   Mateus Seehagen Rodrigues (mrodr107 at calpoly.edu)

from task3B import hmac_sha1

def verify(key, msg, sig_bytes):
    mac = hmac_sha1(key, msg)
    return hmac_sha1(key, mac) == hmac_sha1(key, sig_bytes)

key = "000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f"
message = "Sample #1"

tag = hmac_sha1(key, message)

print verify(key, message, tag)
