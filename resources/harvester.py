#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import subprocess
from subprocess import DEVNULL
from .ui import *

	
# Run and parse results from theHarvester into csv format
def get_harvester_emails(company_domain,harvester_location):
	harvester_emails = []
	# theHarvester's filename is based on a .split; since we use a domain, we parse it out
	company = company_domain.split(".")[0]
	outfile = "/tmp/harvester_{0}_results.xml".format(company)
	print_success("[+] Checking theHarvester...")
	print_success("    (Note: This may take a while)")

	subprocess_cmd = ['python', harvester_location, '-d', company_domain, '-b', 
			'bing,dogpile,google,yahoo', '-f', outfile, '>/dev/null', '2>&1']

	subprocess.check_call(subprocess_cmd, stdout=DEVNULL, stderr=DEVNULL)

	tree = ET.parse(outfile)
	root = tree.getroot()
	for emails in root.findall('email'):
		harvester_emails.append(",,{0},".format(emails.text))
	return harvester_emails