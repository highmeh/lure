#!/usr/bin/env python3
from pyhunter import PyHunter
from .ui import *


# Query HunterIO for email addresses
def get_hunterio_emails(company,API_KEY):
	hunter = PyHunter(API_KEY)
	
	account_info = hunter.account_information()
	calls_remaining = account_info['calls']['left']
	calls_allowed = account_info['calls']['available']
	print_success("[+] Checking hunter.io ({0}/{1} queries remaining)".format(
										calls_remaining, calls_allowed))
	results = hunter.domain_search(company)#, limit=100, emails_type="personal")
	company_records = results['emails']

	hunterio_emails = []
	counter = 0
	for record in company_records:
		email = str(record['value'])
		fname = str(record['first_name'])
		lname = str(record['last_name'])
		position = str(record['position'])
		hunterio_emails.append(fname + "," + lname + "," + email + "," + position)
		counter = counter + 1
	return hunterio_emails
