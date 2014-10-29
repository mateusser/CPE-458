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
    prev_time = max_time
    max_time = 0
    guessed_mac = best_mac
    total_time = 0

    above_average = []
    for j in range(2**8):
        hex_number = '%02x' % (j)
        guessed_mac = guessed_mac[:i] + hex_number + guessed_mac[i + 2:]
        time_mesure = sendMessageAndMac(message, guessed_mac)

        if time_mesure > prev_time:
            total_time += time_mesure
            above_average.append(hex_number)

        if time_mesure == -1:
            get_out_now = True
            break

        if time_mesure > max_time:
            max_time = time_mesure
            best_mac = guessed_mac

    if get_out_now:
        break

    while len(above_average) > 1:
        print
        print
        print "Total of elementes above average ", len(above_average)
        print "Mean:", total_time/len(above_average)
        print

        hex_numbers = above_average
        mean = total_time/len(above_average)

        above_average = []
        total_time = 0
        max_time = 0
        for hexn in hex_numbers:
            guessed_mac = guessed_mac[:i] + hexn + guessed_mac[i + 2:]
            time_mesure = sendMessageAndMac(message, guessed_mac)

            if time_mesure > mean:
                above_average.append(hexn)
                total_time += time_mesure
                print hexn, time_mesure

            if time_mesure == -1:
                get_out_now = True
                break

            if time_mesure > max_time:
                max_time = time_mesure
                best_mac = guessed_mac

        if get_out_now:
            break

    print '\n\nFinal:'
    print max_time
    print best_mac
print
print 'Final MAC: '
print best_mac
