#!/usr/bin/env python3
from .ui import *
import requests
import re


def get_mailshunt_emails(company):
	URL = "https://mailshunt.com/domain-search"
	# start csrf workaround
	client = requests.session()
	client.get(URL)
	source = (client.get(URL).text)

	source_regex = "_token.*> "
	token_from_source = re.findall(source_regex,source)

	split_token = token_from_source[0].split("\"")
	_token = (split_token[2])
	#end CSRF workaround

	if "XSRF-TOKEN" in client.cookies:
		xsrftoken = client.cookies['XSRF-TOKEN']

	if "mailshunt_session" in client.cookies:
		mailshunt_sess = client.cookies['mailshunt_session']

	print_success("[+] Checking MailsHunt")
	search_req = {'_token':_token,'domain':'{0}'.format(company),'XSRF-TOKEN':xsrftoken,'mailshunt_session':mailshunt_sess}
	r = client.post(URL,data=search_req)

	sanitized_emails =[]
	email_unsanitary = "<li class=\"list-group-item\">.*"
	emails_from_source = re.findall(email_unsanitary,r.text)
	for email in emails_from_source:
		fname = ""
		lname = ""
		position = ""
		email = email.split(">")[1]
		sanitized_emails.append(fname + "," + lname + "," + email + "," + position)
	return sanitized_emails