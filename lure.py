#!/usr/bin/env python3
import requests,sys,argparse,csv,os
from gophish import Gophish
from gophish.models import *
from resources import config,hunterio,harvester,bing,webpage
from datetime import datetime
from resources.ui import *

# Suppress certificate verification warnings. 
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# Define the GoPhish API connection
API = Gophish(config.GOPHISH_API_KEY,config.BASE_URL,verify=False)


# Lists resources that Lure can use to search for e-mail addresses
def list_resources():
	gophish_status = check_connection()
	if config.HUNTERIO == True:
		print("  [X] Hunter.io")
	if config.HUNTERIO == False:
		print("  [ ] Hunter.io")
	if config.LINKEDIN == True:
		print("  [X] LinkedIn" + "\t\t\t" + gophish_status)
	if config.LINKEDIN == False:
		print("  [ ] LinkedIn" + "\t\t\t" + gophish_status)
	if config.THEHARVESTER == True:
		print("  [X] TheHarvester")
	if config.THEHARVESTER == False:
		print("  [ ] TheHarvester")
	if config.WEBPAGE == True:
		print("  [X] Scrape Webpage")
	if config.WEBPAGE == False:
		print("  [ ] Scrape Webpage")	
	print_warning("-" * 59)
	print("\n")
		

# Checks if the GoPhish server is online
def check_connection():
	if suppress_gophish:
		gophish_status = success_text + "[+] Ignoring GoPhish." + end_text
		return gophish_status
	if not suppress_gophish:
		try:
			r = requests.get(config.BASE_URL,verify=False,timeout=config.TIMEOUT)
			if r.status_code == 200:
				gophish_status = success_text + "[+] GoPhish Server Online" + end_text
			else:
				gophish_status = fail_text + "[-] GoPhish Server Offline" + end_text
			return gophish_status
		except:	
			gophish_status = fail_text + "[-] GoPhish Server Offline" + end_text
			return gophish_status


# Use the search_email.py module to search common resources for email addresses
def start_discovery(target_company,print_result):
	if config.HUNTERIO == True:
		hunterio_emails = hunterio.get_hunterio_emails(company_domain,config.HUNTERIO_API_KEY)
	if config.HUNTERIO == False:
		hunterio_emails = ""

	if config.THEHARVESTER == True:
		harvester_emails = harvester.get_harvester_emails(
											company_domain,config.HARVESTER_LOCATION)
	if config.THEHARVESTER == False: 
		harvester_emails = ""

	if config.LINKEDIN == True:
		# LinkedIn search is done by company, not domain - split the company off
		company = company_domain.split('.')[0]
		linkedin_emails = bing.scrape_linkedin(company,config.BING_ENDPOINT,config.BING_API_KEY)
		bing_emails = bing.sanitize_results(linkedin_emails,target_company)

	if config.LINKEDIN == False:
		bing_emails = ""

	if config.WEBPAGE == True:
		webpage_emails = webpage.get_webpage_contents(company_domain)

	if config.WEBPAGE == False:
		webpage_emails = ""

	create_master_list(hunterio_emails,harvester_emails,bing_emails,webpage_emails,target_company,print_result)


# Creates a master list of all target info to send to GoPhish
def create_master_list(hunterio_emails,harvester_emails,linkedin_emails,webpage_emails,target_company,print_result):
	assembled_list_contents = []
	master_list_contents = []

	# If the user specified a target file to add to the list, add it now
	if existing_file:
		with open(existing_file,"r") as _existing_file:
			for line in _existing_file:
				line = line.split(",")
				fname = line[0]
				lname = line[1]
				email = line[2]
				position = line[3]
				master_list_contents.append(User(
									first_name=fname,last_name=lname,email=email,position=position))		

	for record in hunterio_emails:
		assembled_list_contents.append(record)

	for record in harvester_emails:
		assembled_list_contents.append(record)

	for record in linkedin_emails:
		assembled_list_contents.append(record)

	for record in webpage_emails:
		assembled_list_contents.append(record)

	counter = 0
	for line in assembled_list_contents:
		try:
			line = line.split(",")
			fname = line[0]
			lname = line[1]
			email = line[2]
			position = line[3]
			excluded = check_exclusions(email)
			if excluded == True:
				print_warning("[!] Exclusion Skipped: {0}".format(email))
				pass
			else:
				master_list_contents.append(User(
											first_name=fname,last_name=lname,email=email,position=position))
				counter = counter + 1
		except:
			pass
			
	if counter == 0:
		print_fail("[-] No targets were found. Check the domain name or add more sources.")
		sys.exit(0)

	print_success("[+] Final list contains {0} targets.".format(counter))
	print_options(master_list_contents,target_company)


def check_exclusions(email):
	with open(exclusion_list, "r") as f:
		for line in f:
			if line.rstrip() == email.rstrip():
				return True
	f.close()

def print_options(master_list_contents,target_company):
	if print_result == True:
		print_success("[+] Printing Target Record Emails:\n")
		for record in master_list_contents:
			print(record.email)

	if print_csv == True:
		print_success("[+] Printing Target CSV:\n")
		print("First Name, Last Name, Position, Email")
		for record in master_list_contents:
			fname = record.first_name
			lname = record.last_name
			email = record.email
			position = record.position
			print(fname + "," + lname + "," + email + "," + position)
	
	if not suppress_gophish:
		upload_targetlist(master_list_contents,company_domain)
	if suppress_gophish:
		sys.exit(0)	


# Creates a GoPhish group object from the master list, and pushes it to the server with generic name
def upload_targetlist(master_list_contents,target_company):
	current_date = datetime.today().strftime('%Y%m%d%H%M%S')
	new_group_name = current_date + "_" + config.TESTER_NAME + "_" + target_company
	new_targetlist = Group(name=new_group_name,targets=master_list_contents)
	try:
		group = API.groups.post(new_targetlist)
		print_success("[+] Target list \'{0}\' (ID: {1}) added!".format(
											new_group_name,group.id,group))
	except Exception as e:
		print_fail("[-] Target list {0} could not be added: {1}".format(new_group_name,e))


# Set up Argparse
progdesc = """ L U R E (Lazy User-Reconnaissance Engine) :: Automate email collection and
			import results into GoPhish. Built by Jayme Hancock (jayme.hancock@bsigroup.com)"""
parser = argparse.ArgumentParser(description=progdesc)
parser.add_argument('-d', metavar='Company Domain', help='Ex: appsecconsulting.com')
parser.add_argument('-f', metavar='Email File', help='Append an existing CSV to search results')
parser.add_argument('-t', action='store_true', help='Create a CSV template file')
parser.add_argument('-v', action='store_true', help='Print version and exit')
parser.add_argument('-p', action='store_true', help='Print emails to stdout')
parser.add_argument('-c', action='store_true', help='Print CSV Formatted data')
parser.add_argument('-x', action='store_true', help='Dont connect to GoPhish, just do the OSINT')
parser.add_argument('-e', metavar='Exclusion File', help='Exclusion file. One email per line.')
args = parser.parse_args()

if args.v:
	print_success(config.VERSION)
	sys.exit(0)

if args.t:
	with open("template.csv","w+") as template:
		template.write("First Name,Last Name,Email,Position\n")
		template.write("John,Smith,jsmith@aol.com,CEO\n")
	template.close()
	print_success("[+] Created GoPhish User Template: template.csv")
	sys.exit(0)

if args.p:
	print_result = True
if not args.p:
	print_result = False

if args.c:
	print_csv = True
if not args.c:
	print_csv = False

if args.x:
	suppress_gophish = True
if not args.x:
	suppress_gophish = False

if args.e:
	exclusion_list = args.e

if args.d:
	company_domain = args.d
	print_logo()
	list_resources()
	if args.f:
		existing_file = args.f
		if os.path.exists(existing_file):
			print_success("[+] Importing {0}...".format(existing_file))
			start_discovery(company_domain,print_result)
		else:
			print_fail("[!] Importing {0} failed; does the file exist?".format(
																existing_file))
			sys.exit(0)
	if not args.f: 
		existing_file = ""
		start_discovery(company_domain,print_result)
	
else:
	print_fail("[-] You must enter a company domain to search!")
	sys.exit(0)