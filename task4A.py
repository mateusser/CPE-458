#!/usr/bin/python
# -*- coding: utf-8 -*-

#Authors:
#   Matheus de Sousa Faria    (desousaf at calpoly.edu)
#   Mateus Seehagen Rodrigues (mrodr107 at calpoly.edu)

import requests
import time

SITE_URL = 'http://localhost:8080'
QUERY_URL = SITE_URL + '/?q={}&mac={}'

query_pattern = 'q={}&mac={}'

def sendMessageAndMac(q, mac):
    url = QUERY_URL.format(q, mac)
    start = time.time()
    req = requests.get(url)
    end = time.time()
    html = req.html

    if 'Invalid signature.' in html:
        return end - start
    else:
        print 'Right MAC: {}'.format(mac)
        print
        print html
        print
        print 'SUCCESS! \o/'
        return True

message = 'Matheus'
guessed_mac = 'a'*40
hex_digit_counter = 0
for i in range(0, 40, 2):
    for j in range(2**8):
        hex_number = '%02x' % (j)
