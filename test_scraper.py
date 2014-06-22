from scraper import parse_source
from scraper import extract_listings
from scraper import read_search_results
from scraper import fetch_search_results


'''i couldn't come up with testing fetch efficiently'''

def test_fetch_results():
    a, b = fetch_search_results(min=900, max=1000, bedrooms=2)
    assert '<!DOCTYPE html>' in a
    assert '<title>seattle apts/housing for rent classifieds' in a
    assert b == 'utf-8'


def test_read_results():
    a = read_search_results()
    assert a[1] == 'utf-8'
    assert isinstance(a[0], str)


def test_parse_source():
    a = str(parse_source("Hello"))
    assert a == u'<html><head></head><body>Hello</body></html>'


def test_extract_listings():
    a = parse_source("<span class='price'>$1450</span>")
    b = extract_listings(a)
    assert len(b) == 0
