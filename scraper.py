from bs4 import BeautifulSoup
import requests
import sys
import json


def fetch_search_results(query=None, min=None, max=None, bedrooms=None):
    search_params = {
        key: val for key, val in locals().items() if val is not None
    }
    if not search_params:
        raise ValueError("No valid keywords")
    base = 'http://seattle.craigslist.org/search/apa'
    resp = requests.get(base, params=search_params, timeout=3)
    resp.raise_for_status()
    return resp.content, resp.encoding


def read_search_results():
    with open('apa.html', 'r') as a:
        data = a.read()
    return data, 'utf-8'


def parse_source(html, encoding='utf-8'):
    parsed = BeautifulSoup(html, from_encoding=encoding)
    return parsed


def extract_listings(parsed):
    location_attrs = {'data-latitude': True, 'data-longitude': True}
    listings = parsed.find_all('p', class_='row')
    for listing in listings:
        location = {key: listing.attrs.get(key, '') for key in location_attrs}
        link = listing.find('span', class_='pl').find('a')
        price_span = listing.find('span', class_='price')
        this_listing = {
            'location': location,
            'link': link.attrs['href'],
            'description': link.string.strip(),
            'price': price_span.string.strip(),
            'size': price_span.next_sibling.strip(' \n-/')
        }
        yield this_listing


def add_address(listing):
    api_url = 'http://maps.googleapis.com/maps/api/geocode/json'
    loc = listing['location']
    latlng_tmpl = "{data-latitude},{data-longitude}"
    parameters = {
        'sensor': 'false',
        'latlng': latlng_tmpl.format(**loc),
    }
    resp = requests.get(api_url, params=parameters)
    resp.raise_for_status() # <- this is a no-op if all is well
    data = json.loads(resp.text)
    if data['status'] == 'OK':
        best = data['results'][0]
        listing['address'] = best['formatted_address']
    else:
        listing['address'] = 'unavailable'
    return listing


if __name__ == '__main__':
    import pprint
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        html, encoding = read_search_results()
    else:
        html, encoding = fetch_search_results(min=500, max=1000, bedrooms=2)
    doc = parse_source(html, encoding)
    for listing in extract_listings(doc):
        listing = add_address(listing)
        pprint.pprint(listing)
