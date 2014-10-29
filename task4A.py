#!/usr/bin/python
# -*- coding: utf-8 -*-

#Authors:
#   Matheus de Sousa Faria    (desousaf at calpoly.edu)
#   Mateus Seehagen Rodrigues (mrodr107 at calpoly.edu)

import requests
import time, os

SITE_URL = 'http://localhost:8080'
QUERY_URL = SITE_URL + '/?q={}&mac={}'

query_pattern = 'q={}&mac={}'

def sendMessageAndMac(q, mac):
    url = QUERY_URL.format(q, mac)
    start = time.time()
    req = requests.get(url)
    end = time.time()
    html = req.text

    if 'Correct!' in html:
        print 'Right MAC: {}'.format(mac)
        print
        print html
        print
        print 'SUCCESS! \o/'
        return -1
    else:
        return end - start

message = 'Matheus'
best_mac = guessed_mac = 'a'*40

max_time = 0
get_out_now = False

for i in range(0, 40, 2):
    prev_time = max_time
    guessed_mac = best_mac
    max_time = 0

    for j in range(2**8):
        hex_number = '%02x' % (j)
        guessed_mac = guessed_mac[:i] + hex_number + guessed_mac[i + 2:]
        time_mesure = sendMessageAndMac(message, guessed_mac)

        if time_mesure == -1:
            get_out_now = True
            break

        if time_mesure > max_time:
            max_time = time_mesure
            best_mac = guessed_mac
            choosen_hex = hex_number

    print i
    print best_mac, max_time
    print

print
print 'Final MAC: '
print best_mac
