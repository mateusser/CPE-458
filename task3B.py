import cookielib
import requests
import urllib, urllib2

from core_crypto import *
from conversions import *

SITE_URL = 'http://localhost:8080'
REGISTER_URL = 'http://localhost:8080/register'
HOME_URL = 'http://localhost:8080/home'
LOGOUT_URL = 'http://localhost:8080/logout'

MY_USERNAME = 'matheusssss' + 'admin' + chr(0)*11 + chr(12)
MY_USERNAME = 'matheus'
MY_PASSWORD = '123456'
MY_ROLE = 'user'
TARGET_ROLE = 'admin'
TARGET_COOKIE = 'auth_token'

cookie_pattern = 'user={}&uid={}&role={}'
session = requests.Session()


def register(username, password):
    register_form = {
        'user': username,
        'password': password,
    }

    register_page_html = urllib2.urlopen(REGISTER_URL, urllib.urlencode(register_form))
    html = register_page_html.read()

    if 'User registered' in html:
        print '{} registered...'.format(username)
    elif 'User already registered' in html:
        print '{} already registered...'.format(username)
    else:
        print 'Invalid page...'

def getAuthCookie(username, password):
    access_form = {
        'user': username,
        'password': password,
    }

    session.post(SITE_URL, data = access_form)

    original_cookie = session.cookies[TARGET_COOKIE]

    session.get(LOGOUT_URL)

    return original_cookie

def flip_block(e_block, pt_block, wanted_block):
    result_block = ''
    for index in range(len(e_block)):
        result_block += chr(ord(e_block[index]) ^ ord(pt_block[index]) ^ ord(wanted_block[index]))
    return result_block

def printMessageInBlocks(message, block_size):
    for i in range(len(message)/block_size + 1):
        print '[',
        print message[i*block_size:(i*block_size)+block_size],
        print ']'


username = 'mathsssssss'
print 'Registring user1...'
register(username, MY_PASSWORD)
print
print '{} guessed session cookie:'.format(username)
printMessageInBlocks(cookie_pattern.format(username, 1, MY_ROLE), 16)

username2 = 'mathssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss'
print '\nRegistring user2...'
register(username2, MY_PASSWORD)
print
print '{} guessed session cookie:'.format(username2)
printMessageInBlocks(cookie_pattern.format(username2, 2, MY_ROLE), 16)

print '\nUser2 real encoded session cookie:'
original_cookie = getAuthCookie(username2, MY_PASSWORD)

printMessageInBlocks(original_cookie, AES.block_size*2)

original_cookie = hex_to_ascii(original_cookie)
print '\nFliping user to {}, uid to 1, role to admin'.format(username)
blocks = []
for i in range(len(original_cookie)/16):
    blocks.append(original_cookie[i*16:i*16 + 16])

blocks[0] = flip_block(blocks[0], 'user=mathsssssss', 'user=mathssssss&')
blocks[2] = flip_block(blocks[2], 's'*16, '&uid=1&xxxxxxxxx')
blocks[4] = flip_block(blocks[4], 'sssssss&uid=1&ro', '&role=admin&zzzz')

flipped_cookie = ''.join(blocks)
flipped_cookie_encoded = ascii_to_hex(flipped_cookie)

print '\nHow the cookie should look like'
print '''
[  iv-trash---line ]
[ user=mathssssss& ]
[   trash---line   ]
[ &uid=1&xxxxxxxxx ]
[   trash---line   ]
[ &role=admin&xxxx ]
[ e=user ]
'''

print 'Cookie generated:'
printMessageInBlocks(flipped_cookie_encoded, 32)
print
print flipped_cookie_encoded

my_cookies = {TARGET_COOKIE: flipped_cookie_encoded}
response = session.get(HOME_URL, cookies = my_cookies)
print
print
print response.text
print
print
if 'Welcome, Admin!' in response.text:
    print 'SUCCESS!'
