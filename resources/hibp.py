#!/usr/bin/env python3
import json
import requests
from .ui import print_fail
import time

def check_email_in_hibp(email,hibp_app,hibp_api_key):
	headers = {"hibp-api-key":hibp_api_key,"user-agent":hibp_app}
	url = "https://haveibeenpwned.com/api/v3/breachedaccount/{0}".format(email)
	breaches = []
	r = requests.get(url, headers=headers)
	time.sleep(0.5)
	breachdata = json.loads(r.text)
	for breach in breachdata:
		breaches.append(breach['Name'])
	print_fail("[-] {0} has been pwned! Breach(es): {1}".format(email,', '.join(str(x) for x in breaches)))
	return