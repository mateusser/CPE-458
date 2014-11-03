#!/usr/bin/python
# -*- coding: utf-8 -*-

#Authors:
#   Matheus de Sousa Faria    (desousaf at calpoly.edu)
#   Mateus Seehagen Rodrigues (mrodr107 at calpoly.edu)

import requests
import time, os

from conversions import *

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

def get_dict_top_elements(dictionary, how_many):
    if how_many == -1:
        how_many = len(dictionary)
    pairs = dictionary.items()
    sorted_pairs = sorted(pairs, key=lambda pair: pair[1], reverse=True)
    return sorted_pairs[:how_many]

def list_with_tuples_to_dict(list_with_tuples):
    dictionary = {}
    for item in list_with_tuples:
        dictionary[item[0]] = item[1]
    return dictionary

def print_dict(dictionary):
    for key in dictionary:
        print key, dictionary[key]

def mac_guesser(message, start_point, start_mac):
    get_out_now = False
    most_possible_mac = ''
    safe_index = 0
    multiple_macs = 20

    all_macs = {}
    for i in range(multiple_macs):
        all_macs[start_mac[:-2] + '%02d' % i] = 0

    for i in range(start_point, 40, 2):
        print '='*80
        print i
        print

        new_all_macs = {}
        for mac, count in zip(all_macs, range(multiple_macs)):
            new_all_macs[mac[:-2] + '%02d' % count] = all_macs[mac]
        all_macs = new_all_macs

        best_10_macs = all_macs

        print_dict(best_10_macs)
        print

        all_best_macs = {}
        for mac in best_10_macs:
            print '-' * 60
            print 'MAC to evaluate:', mac

            guessed_mac = mac
            all_macs = {}
            for j in range(2**8):
                hex_number = '%02x' % (j)
                guessed_mac = guessed_mac[:i] + hex_number + guessed_mac[i + 2:]
                time_mesure = sendMessageAndMac(message, guessed_mac)

                all_macs[guessed_mac] = time_mesure

                if time_mesure == -1:
                    get_out_now = True
                    break

            if get_out_now:
                break

            top_10 = list_with_tuples_to_dict(get_dict_top_elements(all_macs, multiple_macs))
            all_best_macs.update(top_10)

            print 'Best {} for this mac:'.format(multiple_macs)
            print_dict(top_10)
            print

        if get_out_now:
            break


        mean = 0
        for mac in all_best_macs:
            mean += all_best_macs[mac]/len(all_best_macs)

        above_mean = 0
        count_elements = 0
        for mac in all_best_macs:
            if all_best_macs[mac] >= mean:
                above_mean += all_best_macs[mac]
                count_elements += 1

        above_mean_dict = {}
        for mac in all_best_macs:
            if all_best_macs[mac] >= mean and all_best_macs[mac] <= above_mean:
                above_mean_dict[mac] = all_best_macs[mac]

        if i == 0:
            all_macs = list_with_tuples_to_dict(get_dict_top_elements(above_mean_dict, -1)[:-multiple_macs])
        else:
            all_macs = list_with_tuples_to_dict(get_dict_top_elements(above_mean_dict, multiple_macs))

        broke = False
        for jj in range(0, i + 2, 2):
            previous_mac = ''
            for mac in all_macs:
                if mac[:jj + 2] == previous_mac or previous_mac == '':
                    previous_mac = mac[:jj + 2]
                else:
                    broke = True
                    break
            if broke:
                most_possible_mac = previous_mac[:jj]
                if most_possible_mac != '':
                    most_possible_mac = most_possible_mac.ljust(40, 'a')
                safe_index = jj
                break

        print
        print i, '-- Most possible MAC until now:', most_possible_mac
        print 'Safe Index: ', safe_index
        print
    return most_possible_mac, safe_index, get_out_now

message = 'Matheus'
most_possible_mac = 'a'*40
safe_index = 0
while True:
    most_possible_mac, safe_index, get_out_now = mac_guesser(message, safe_index, most_possible_mac)
    if get_out_now:
        break

