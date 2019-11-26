import requests
import json
import sys
from .ui import print_success
from requests.auth import HTTPBasicAuth


def find_github_emails(organization,organization_domain,github_api,github_username,github_token):
	github_emails = []
	print_success("[+] Searching GitHub")
	page_number = 1
	while page_number < 2:
		orgquery = requests.get((github_api + "/orgs/{0}/members?per_page=100&page={1}".format(
						organization,page_number)), auth=HTTPBasicAuth(github_username,github_token))
		results = json.loads(orgquery.text)
		for result in results:
			try:
				username = result["login"]
				userquery = requests.get((github_api + "/users/{0}".format(username)), 
											auth=HTTPBasicAuth(github_username,github_token))
				userdata = json.loads(userquery.text)
				email = userdata["email"]
				if email:
					check_domain = email.split("@")
					if check_domain[1] == organization_domain:
						github_emails.append(",,{0},".format(email))
			except:
				break
		page_number += 1

	return github_emails
