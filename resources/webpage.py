#!/usr/bin/env python3
import requests
import re
from html.parser import HTMLParser
from .ui import *


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

# Scrape common web locations for email addresses
def get_webpage_contents(company):
	print_success("[+] Checking common webpage locations")
	scraped_webpage_emails = []
	urls_to_check = ["/","/contact","/contactus","/about","/aboutus","/careers",
					"/ourcompany","/company","/ourteam","/team","/about-us", 
					"/our-team", "/contact-us", "/our-company"]
	for url_to_check in urls_to_check:
		url = "http://www.{0}{1}".format(company,url_to_check)
		try:
			r = requests.get(url)
			if not 200 in r.status_code:
				print_fail("[-] Domain could not be reached.")
			if r.status_code == 200:
				webcontent = strip_tags(r.text)
				emails = re.findall('\S+@\S+', webcontent)

				for email in emails:
					scraped_webpage_emails.append(", , ," + email + ",")
			else:
				print("Not found: {0}".format(url_to_check))
		except:
			pass

	return scraped_webpage_emails