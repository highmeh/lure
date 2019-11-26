# LURE
Lure - User Recon Automation for GoPhish
  
  
## What is Lure?
Lure assists in phishing target collection by pulling and parsing email addresses for a target organization. The results are normalized into a format recognized by GoPhish, and then uploaded to the server.  
  
## What sources does Lure search?  
Lure currently searches the following, but more sources are being added all the time. 
|          Source          | Authenticated |
|--------------------------|---------------|
| Hunter.io                |      Yes      |
| theHarvester             |      No       |
| LinkedIn*                |      Yes      |
| MailsHunt                |      No       |
| Common website Locations |      No       |
  

 * LinkedIn searching leverages the Bing API, Not the LinkedIn API.

## Why do some sources require an API Key?
Where possible and practical, Lure uses web scraping to eliminate the need of API Keys. However, some services have provide better options in terms of number of results, lack of throttling, or access to additional information when an API key is used. By default, config.py uses only unauthenticated sources. We *highly* recommend registering for the services that use API keys, as most offer free accounts and will give you much better results.

## How do I run Lure?  
- Clone the git repo: ``git clone https://github.com/highmeh/lure/lure.git``
- Install the prerequisites: ``pip3 install -r requirements.txt``
- Edit config.py to ensure your API keys and paths are correct.
- Give lure a domain to search and wait:
  - ``./lure.py -d microsoft.com``

## What if I already have a list of targets?
You can use the ``./lure.py -d domain.com -f /path/to/file.csv`` options to import a csv file in GoPhish format. Lure will append any search results to that list before uploading it.

## What is the Gophish Format for the CSV?
Use ``./lure.py -t`` to generate a CSV template.

## Can I customize which sources Lure uses?
Yes, edit resources/config.py and change the sources to "True" or "False"

## Lure is taking a long time to complete.
Disable theHarvester in resources/config.py. theHarvester takes a long time to generate very few results. 

## What if I want to use lure For OSINT, but not phishing?
Lure was designed to be used along side GoPhish, but some users understandably wanted to use it for OSINT only. As of version 0.3, you can use the "-x" switch to ignore the GoPhish server options entirely and just perform email collection.

## How do I get a list of my results?
Use "-c" for Comma-Separated Value output, or "-p" to print e-mail addresses only.

## How do I exclude pre-defined/out of scope users from ending up in a contact list?
Create an exclusions file. Add the emails you want to exclude, one per line, into a text file and run lure with the "-e file.txt" option.

## Where do I enter API keys, tester names, and other variables?
Edit resources/config.py. You can run ``mv resources/config.sample.py resources/config.py`` to fill in the configuration template.

## Lure says it found X number of emails, but the GoPhish group shows a different number.
GoPhish will not accept invalid entries. If one of the email addresses is collected erroneously and ends up being "username@something@domain.com", "u....sername@domain.com", etc, it will be rejected during the upload. It also uses excludes duplicate emails.

## Screenshots
![Lure Command Line](https://github.com/highmeh/lure/blob/master/screenshots/lure_cli.png?raw=true)

![Lure Importing to GoPhish](https://github.com/highmeh/lure/blob/master/screenshots/lure_gophish.png?raw=true)

## CHANGELOG
20191028: v0.2 Released. Adds function to print records to stdout (-p flag). Adds in webpage email scraping for common webpage locations (on by default). Built in some error logic for domains that are invalid or return no results.

20191122: v0.3 Released. Suppress the upload to GoPhish (OSINT Only Mode) (-x). Exclude emails from an exclusion list (-e excludes.txt). Print emails only (-p). Print CSV Contents (-c).

20191125: v0.4 Released. Adds support for MailsHunt and for GitHub searches. Reorganized config.sample.py for easier reading/parsing. Minor bug fixes.
