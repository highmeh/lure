# LURE
Lure - User Recon Automation for GoPhish
  
  
## What is Lure?
Lure assists in phishing target collection by pulling and parsing email addresses for a target organization. The results are normalized into a format recognized by GoPhish, and then uploaded to the server.  
  
## What sources does Lure search?  
Lure currently searches the following sources:
- Hunter.io
- theHarvester
- LinkedIn (via Bing Search API)

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

## Where do I enter API keys, tester names, and other variables?
Edit resources/config.py. You can run ``mv resources/config.sample.py resources/config.py`` to fill in the configuration template.

## Lure says it found X number of emails, but the GoPhish group shows a different number.
GoPhish will not accept invalid entries. If one of the email addresses is collected erroneously and ends up being "username@something@domain.com", "u....sername@domain.com", etc, it will be rejected during the upload.

## Screenshots
![Lure Command Line](https://github.com/highmeh/lure/blob/master/screenshots/lure_cli.png?raw=true)

![Lure Importing to GoPhish](https://github.com/highmeh/lure/blob/master/screenshots/lure_gophish.png?raw=true)

## CHANGELOG
20191028: v0.2 Released. Adds function to print records to stdout (-p flag). Adds in webpage email scraping for common webpage locations (on by default). Built in some error logic for domains that are invalid or return no results.