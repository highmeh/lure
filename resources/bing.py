#!/usr/bin/env python3
import requests
import json
import re
from .ui import *


linkedin_emails = []


# Use Bing Search API to query 
def scrape_linkedin(company,bing_endpoint,bing_api_key):
	result_names = []
	headers = {'Ocp-Apim-Subscription-Key':bing_api_key}
	print_success("[+] Checking LinkedIn (via Bing Search)")
	search = " intitle:LinkedIn&customconfig=9ba316ca-9c01-40f4-b45f-d3272abb0af1&mkt=en-US&count=50"
	url = (bing_endpoint + company + search)
	r = requests.get(url, headers=headers)

	content = json.loads(r.text)
	for page in content['webPages']['value']:
		name = page['name']
		name = re.sub(" - .*", "", name)
		name = re.sub("'", "", name)
		name = re.sub("-", "", name)
		result_names.append(name)

	return(result_names)

# Strip out commonly used phrases in advertisements and non-People results
def sanitize_results(result_names,company_domain):
	for person in result_names:
		if ("Best" in person or "Jobs" in person or "Hiring" in person or 
			"Top" in person or "hiring" in person or "Salaries" in person or
			"New" in person):
			result_names.remove(person)

	# Format the results into a flast@domain.com format - TODO: add additional formats
	for name in result_names:
		name = name.split(" ")
		if(len(name) >= 2): 
			fname = name[0]
			lname = name[1]
			domain = company_domain
			email = fname[0] + lname + "@" + domain
			linkedin_emails.append(fname + "," + lname + "," + email + ",None")

	return linkedin_emails