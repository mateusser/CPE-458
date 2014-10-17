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

cookie_pattern = 'user={}&uid=2&role={}'
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

def printMessageInBlocks(message, block_size):
    for i in range(len(message)/block_size + 1):
        print '[',
        print message[i*block_size:(i*block_size)+block_size],
        print ']'



# Creating the first username, has to be the size of two blocks
# First Block:  user=matheusssss
# Second Block: admin00000000000 -> ANSI x.923 pad
admin_block = TARGET_ROLE + (chr(0)*(AES.block_size - len(TARGET_ROLE) - 1)) + chr(AES.block_size - len(TARGET_ROLE))
username1 = MY_USERNAME + MY_USERNAME[-1]*(AES.block_size - len('user=' + MY_USERNAME)) + admin_block

print 'Registring user1...'

register(username1, MY_PASSWORD)

print 'User1 cookie message:'
printMessageInBlocks(cookie_pattern.format(username1, MY_ROLE), AES.block_size)

print '\nUser1 cookie:'
original_cookie = getAuthCookie(username1, MY_PASSWORD)

printMessageInBlocks(original_cookie, AES.block_size*2)

print '\nGet admin0000... information block'
admin_block_cookie = original_cookie[AES.block_size*2:AES.block_size*4]
print admin_block_cookie

print
# Creating the second username, has to left the last line of
# the message, just with the role
# First Block:  user=matheusssss
# Second Block: ssss&uid=2&role=
# Third Block:  user
username2 = MY_USERNAME + MY_USERNAME[-1]*(AES.block_size - len('user=' + MY_USERNAME) + len(MY_ROLE))

print 'Registring user2...'

register(username2, MY_PASSWORD)
print 'User2 cookie message:'
printMessageInBlocks(cookie_pattern.format(username2, MY_ROLE), AES.block_size)

print '\nUser2 cookie:'
original_user2_cookie = getAuthCookie(username2, MY_PASSWORD)

printMessageInBlocks(original_user2_cookie, AES.block_size*2)

print
print
print 'Generate the new cookie with admin block...'
admin_cookie_auth = original_user2_cookie[:AES.block_size*4] + admin_block_cookie
printMessageInBlocks(admin_cookie_auth, AES.block_size*2)

print 'Generated cookie...'
print admin_cookie_auth
print
print 'Loggin with the cookie...'
my_cookies = {TARGET_COOKIE: admin_cookie_auth}
response = session.get(HOME_URL, cookies = my_cookies)
print
print
print response.text
print
print
if 'Welcome, Admin!' in response.text:
    print 'SUCCESS!'
