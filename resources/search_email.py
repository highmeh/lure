#!/usr/bin/env python3
from pyhunter import PyHunter
import xml.etree.ElementTree as ET
import os


# Define text styling
end_text = "\033[0m"
warning_text = "\033[93m"
success_text = "\033[92m"
fail_text = "\033[91m"


# Query HunterIO for email addresses
def get_hunterio_emails(company,API_KEY):
	hunter = PyHunter(API_KEY)
	
	account_info = hunter.account_information()
	calls_remaining = account_info['calls']['left']
	calls_allowed = account_info['calls']['available']
	print(success_text + "[+] Checking hunter.io ({0}/{1} queries remaining)".format(
										calls_remaining, calls_allowed) + end_text)
	results = hunter.domain_search(company, limit=10, emails_type="personal")
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
	
# Run and parse results from theHarvester into csv format
def get_harvester_emails(company_domain,harvester_location):
	harvester_emails = []
	# theHarvester's filename is based on a .split; since we use a domain, we parse it out
	company = company_domain.split(".")[0]
	outfile = "/tmp/harvester_{0}_results.xml".format(company)
	print(success_text + "[+] Checking theHarvester...")
	print("    (Note: This may take a while)" + end_text)
	
	subprocess_cmd = "python {0} -d {1} -b bing,dogpile,google,yahoo -f {2} >/dev/null 2>&1".format(
					 									harvester_location,company_domain,outfile)
	os.system(subprocess_cmd)
	
	tree = ET.parse(outfile)
	root = tree.getroot()
	for emails in root.findall('email'):
		harvester_emails.append(",,{0},".format(emails.text))
	return harvester_emails

