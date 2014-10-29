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
    print '\n\n'
    print '='*80
    print i

    prev_time = sendMessageAndMac(message, best_mac)
    guessed_mac = best_mac
    total_time = 0
    max_time = 0

    hex_dict = {}
    for k in range(30):
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

        if choosen_hex in hex_dict:
            hex_dict[choosen_hex] += 1
        else:
            hex_dict[choosen_hex] = 1

        print best_mac, max_time

        if get_out_now:
            break

    print
    print hex_dict
    print
    maxn = 0
    for hex_number in hex_dict:
        if hex_dict[hex_number] > maxn:
            choosen_hex = hex_number
            maxn = hex_dict[hex_number]
    best_mac = guessed_mac[:i] + choosen_hex + guessed_mac[i + 2:]

    print '\n\nFinal:'
    print max_time
    print best_mac
print
print 'Final MAC: '
print best_mac
