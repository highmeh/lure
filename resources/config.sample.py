# SERVER CONFIG
GOPHISH_API_KEY = "<<api key>>"
GOPHISH_SERVER = "https://<<phishingserver>>"
GOPHISH_PORT = 3333
TESTER_NAME = "<<configure me>>"
BASE_URL = GOPHISH_SERVER + ":" + str(GOPHISH_PORT)

#API ENDPOINT CONFIG
GITHUB_ENDPOINT = "https://api.github.com"
BING_ENDPOINT = "https://api.cognitive.microsoft.com/bingcustomsearch/v7.0/search?q="

#APIKEY CONFIG - You'll need to add your API Keys here to do authenticated searches.
HUNTERIO_API_KEY = "<<api key>>"
BING_API_KEY = "<<api key>>"
GITHUB_USERNAME	  = "<<github username>>"
GITHUB_API_KEY = "<<github api key>>"

# DISCOVERY CONFIG - Change these to True or False to search/exclude sources
#					 By default, only unauthenticated web searches are enabled.
HUNTERIO = False
THEHARVESTER = False
LINKEDIN = False
WEBPAGE = True
GITHUB = False

# MISC - You shouldn't need to change these.
TIMEOUT = 5
HARVESTER_LOCATION = "/usr/share/theHarvester/theHarvester.py"
VERSION = "Lure v0.4"
