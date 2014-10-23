import os
import re
import urllib, urllib2

from conversions import *
from core_crypto import *

SITE_URL = 'http://localhost:8080'
CIPHER_URL = SITE_URL + '/eavesdrop'
SUBMIT_URL = SITE_URL + '/submit'
CHECK_URL = SITE_URL + '/?enc={}'

block_size = 16

def get_cipher():
    cipher_page_html = urllib2.urlopen(CIPHER_URL)
    regex = re.compile(r'''<p><font color="black"> You eavesdropped the following message: </font></p>\s*<p><font color="red"> (.*) </font></p>''')
    html = cipher_page_html.read()
    return regex.findall(html)[0]


def check_cipher(ciphertext):
    try:
        urllib2.urlopen(CHECK_URL.format(ciphertext))
    except urllib2.HTTPError, error:
        if error.code == 404:
            return True
        return False

def check_guess(plaintext):
    guess_form = {
        'guess': plaintext,
    }

    guess_page_html = urllib2.urlopen(SUBMIT_URL, urllib.urlencode(guess_form))
    html = guess_page_html.read()
    print html
    if 'Correct!' in html:
        return True
    return False


print 'Getting ciphertext...'
ciphertext = get_cipher()
print ciphertext
print

ct_decoded = hex_to_ascii(ciphertext)
ct_blocks = get_message_in_blocks(ct_decoded, block_size)

plaintext = ''
for index_block in range(len(ct_blocks) - 1):
    internal_state = ''
    for internal_index in range(1, block_size + 1):
        for i in range(256):
            fake_block = os.urandom(block_size - internal_index) + chr(i)

            for char in internal_state:
                fake_block += chr(internal_index ^ ord(char))

            ct_blocks[len(ct_blocks) - (index_block + 2)] = fake_block
            if check_cipher(ascii_to_hex(''.join(ct_blocks[:len(ct_blocks) - (index_block)]))):
                internal_state = chr(i ^ internal_index) + internal_state
                break
    ct_blocks = get_message_in_blocks(ct_decoded, block_size)
    plaintext = xor_strings(internal_state, ct_blocks[len(ct_blocks) - (index_block + 2)]) + plaintext

plaintext = plaintext[:-1*ord(plaintext[-1])]

print plaintext
print
print 'Checking text found...'
if check_guess(plaintext):
    print 'SUCCESS! \o/'
else:
    print 'FAIL =('
