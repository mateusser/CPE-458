import cookielib
import requests
import urllib, urllib2

from core_crypto import *
from conversions import *

SITE_URL = 'http://localhost:8080'
REGISTER_URL = 'http://localhost:8080/register'
HOME_URL = 'http://localhost:8080/home'
LOGOUT_URL = 'http://localhost:8080/logout'

MY_USERNAME = 'matheus'
MY_USERNAME = 'aaaaaaaaaaaadmin00000000000nnnn'
MY_PASSWORD = '123456'
MY_ROLE = 'admin'

print 'Registring a new user...'

register_form = {
    'user': MY_USERNAME,
    'password': MY_PASSWORD,
}

register_page_html = urllib2.urlopen(REGISTER_URL, urllib.urlencode(register_form))
html = register_page_html.read()

if 'User registered' in html:
    print '{} registered...'.format(MY_USERNAME)
elif 'User already registered' in html:
    print '{} already registered...'.format(MY_USERNAME)
else:
    print 'Invalid page...'

print 'Access Account...'

access_form = {
    'user': MY_USERNAME,
    'password': MY_PASSWORD,
}

session = requests.Session()
session.post(SITE_URL, data = access_form)

target_cookie = 'auth_token'
cookie_pattern = 'user={}&uid={}&role={}'.format(MY_USERNAME, 2, MY_ROLE)

print '{} cookie on {} home page:'.format(target_cookie, MY_USERNAME)
original_cookie = session.cookies[target_cookie]
print original_cookie

original_cookie_decoded = hex_to_ascii(original_cookie)

print 'Changing the role to admin...'
role_start = len(cookie_pattern) - len(MY_ROLE)
role_end = len(cookie_pattern)

for i in range(len(cookie_pattern)/AES.block_size + 1):
    print cookie_pattern[i*AES.block_size:(i*AES.block_size)+AES.block_size]
for i in range(len(original_cookie_decoded)/AES.block_size + 1):
    print original_cookie_decoded[i*AES.block_size:(i*AES.block_size)+AES.block_size]

#print cookie_pattern[role_start: role_end]
role = original_cookie_decoded[role_start: role_end]
role = ascii_to_hex(original_cookie_decoded[37:37 + len('admin')])

admin_role_cookie = ascii_to_hex(
    original_cookie_decoded[:role_start] +
    role +
    original_cookie_decoded[role_end:]
)

session.get(LOGOUT_URL)
my_cookies = {target_cookie: admin_role_cookie}
response = session.get(SITE_URL, cookies = my_cookies)
if 'Already logged in' in response.text:
    print 'SUCCESS!'
