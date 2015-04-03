from fuzzywuzzy import fuzz, process
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from bs4 import BeautifulSoup
import sys
import requests
import socket

# Process arguments
if len(sys.argv) != 2:
    sys.exit("format: sgets [URL]")
url = sys.argv[1]

validate = URLValidator(schemes=['http', 'https'])
try:
    validate(url)
except:
    sys.exit("Validation error: please provide http or https")

try: 
    response = requests.get(url)
except:
    sys.exit("url invalid")

try: 
    assert response.status_code < 400
except AssertionError:
    sys.exit(url, " unreachable")

soup = BeautifulSoup(response.text)
for link in soup.find_all('a'):
    if twitter(link):
        print(link.get('href'))

def twitter(link):
    return True