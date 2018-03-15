#!/usr/bin/python
# @mealpalinator.py: Mealpal auto reservation like a boss
# @author: jerold@v00d00sec.com
# @version: 0.1a

import argparse
import requests
import json
import os
import sys
import datetime
import subprocess
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# temporary hackish attempt at avoiding any encoding issues in python 2.7
reload(sys)
sys.setdefaultencoding('utf-8')

# argparse stuff
parser = argparse.ArgumentParser(description='Mealpal auto reservation like a boss.')
parser.add_argument('-u','--user-cookie',action='store',dest='cookie',default=None,help='MOBILE APP COOKIE',required=True)
parser.add_argument('-d','--date',action='store',dest='date',default=None,help='YYYYMMDD',required=True)
parser.add_argument('-s','--shop',action='store',dest='shop',default=None,help='SHOP NAME',required=True)

results = parser.parse_args()
USER_COOKIE = results.cookie
DATE = results.date
SHOP = results.shop
BASE_URL = 'https://api.mealpal.com'

def auth():
	print '[+] Attempting to authenticate to Mealpal using provided cookie...'
	cookie = '_mealpal_session=' + USER_COOKIE
	global HEADERS
	HEADERS = {'Cookie' : cookie}
	r = requests.post(BASE_URL + '/1/functions/getCurrentUser', headers=HEADERS, verify=False)
	if r.status_code == 200:
		parsed_json = json.loads(r.content)
		first_name = parsed_json['result']['firstName']
		last_name = parsed_json['result']['lastName']
		print '[+] Authenticated as: ' + first_name + ' ' + last_name
		return 1
	else:
		return 0

def reserve_food(shop_id):
	print '[+] Attempting to reserve some food like a boss...'
	r = requests.post(BASE_URL + '/api/v2/reservations', headers=HEADERS,json={"schedule_id":shop_id, "pickup_time":"12:00pm-12:15pm","kitchen_mode":"flex","quantity":"1","source":"iOS 2.12.1.6"}, verify=False)
	if r.status_code == 200:
		parsed_json = json.loads(r.content)
		order_number = parsed_json['result']['schedule']['order_number']
		meal_name = parsed_json['result']['schedule']['meal']['name']
		print '[+] Done! You ordered ' + meal_name + ' and the order number is: ' + order_number + '.\n'
	else:
		print '[!] Problem with reservation. Server returned the following code: ' + str(r.status_code) + ' ' + r.content

def get_foodlist():
	print '[+] Getting today\'s food list...'
	r = requests.get(BASE_URL + '/api/v2/cities/00000000-1000-4000-9091-919aa43e4747/dates/' + str(DATE) + '/product_offerings/lunch/menu?source=iOS%202.12.1.6', headers=HEADERS, verify=False)
	if r.status_code == 200:
		parsed_json = json.loads(r.content)
		array_data = list(parsed_json.values())

def get_shop_id():
	print '[+] Getting ' + SHOP + '\'s schedule ID...'
	r = requests.get(BASE_URL + '/api/v2/cities/00000000-1000-4000-9091-919aa43e4747/dates/' + str(DATE) + '/product_offerings/lunch/menu?source=iOS%202.12.1.6', headers=HEADERS, verify=False)
	if r.status_code == 200:
		parsed_json = json.loads(r.content)
		prettified = json.dumps(parsed_json, indent=4)
		with open ('tmp.txt', 'w') as outfile:
			outfile.write(prettified)
		grep_cmd = 'cat tmp.txt | grep -A 16 \''+ SHOP +'\' | tail -1'
		raw_shop_id = subprocess.check_output(grep_cmd, shell=True).strip()
		shop_uuid = re.compile('[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}').findall(raw_shop_id)
		shop_uuid = ''.join(shop_uuid)
		try:
			os.remove('tmp.txt')
		except OSError:
			pass
		if shop_uuid != '':
			print '[+] ' + SHOP + '\'s schedule id for ' + DATE + ' is: ' + shop_uuid
			return shop_uuid
		else:
			print '[+] There is no '+ SHOP +' available on ' + DATE
			sys.exit()
	else:
		print '[+] Problem encountered when searching for ' + SHOP + '\'s schedule ID on ' + DATE + ', schedule is probably not out yet.'
		sys.exit()
		
def main():

	if auth() == 1:
		shop_id = get_shop_id()
		reserve_food(shop_id)
	else:
		print '[+] Cookie is no longer valid. Please obtain a new one and try again.\n'

print '\n[*] mealpalinator v0.1a - jerold@v00d00sec.com'
main()