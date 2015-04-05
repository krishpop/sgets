from fuzzywuzzy import fuzz, process
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from bs4 import BeautifulSoup
import sys
import re
import json
import requests
import thread

social_domains = [r'twitter.com/', r'facebook.com/']

google_domain = r'play.google.com/store/apps/details?id='

apple_pattern = r'itunes.apple.com/app/'

twitter_pattern = re.compile(
    r'^(?:http)s?://'
    r'(?:www.)?' + social_domains[0] +
    r'([a-zA-Z0-9_]{1,15})/?'
    )

facebook_pattern = re.compile(
    r'^(?:http)s?://'
    r'(?:www.)?' + social_domains[1] +
    r'([a-zA-Z0-9_]{1,15})/?'
    )

google_pattern = re.compile(
    r'^(?:http)s?://'
    r'(?:www.)?' + google_domain +
    r'([a-zA-Z0-0_.]+)'
    )

ios_pattern = re.compile(
    r'^(?:http)s?://'
    r'(?:www.)?' + apple_domain +
    r'([a-zA-Z0-0_.\-]+)/id'
    r'([0-9]{9})'
    )


def find_id(link, pattern_to_match, pattern_match, url_domain):
    user_match = pattern_to_match.match(link)
    if user_match:
        username = user_match.group(1)
        match_score = fuzz.ratio(username, url_domain)
        if match_score > pattern_match[1]:
            return (username, match_score)
    return pattern_match


def get_domain(url):
    return "zynga"


def validate_url(url):
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
    return response


def main():
    # Process arguments
    if len(sys.argv) != 2:
        sys.exit("format: sgets [URL]")
    url = sys.argv[1]
    response = validate_url(url)
    url_domain = get_domain(url)

    soup = BeautifulSoup(response.text)
    twitter_match = (None, -1)
    for link in soup.find_all('a'):
        link_url = link.get('href')
        twitter_match = find_id(
            link_url, twitter_pattern, twitter_match, url_domain)
        facebook_match = find_id(
            link_url, facebook_pattern, facebook_match, url_domain)
        ios_match = find_id(link_url, ios_pattern, ios_match, url_domain)
        google_match = find_id(link_url, google_pattern, google_match,
                               url_domain)
    print(twitter_match)
    print(facebook_match)
    print(ios_match)
    print(google_match)

if __name__ == '__main__':
    main()
