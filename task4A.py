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
for i in range(0, 40, 2):
    max_time = 0
    total_time = 0
    guessed_mac = best_mac

    for j in range(2**8):
        hex_number = '%02x' % (j)
        guessed_mac = guessed_mac[:i] + hex_number + guessed_mac[i + 2:]
        time_mesure = sendMessageAndMac(message, guessed_mac)
        total_time += time_mesure

        if time_mesure == -1:
            break

        if time_mesure > max_time:
            max_time = time_mesure
            best_mac = guessed_mac
    print i
    print max_time
    print best_mac
    time.sleep(.02)
print best_mac
