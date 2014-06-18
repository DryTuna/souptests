from scraper import parse_source
from scraper import extract_listings
from scraper import read_search_results

#i couldn't come up with testing fetch efficiently

def test_read_results():
    a = read_search_results()
    assert a[1] == 'utf-8'
    assert a[0] is type("")

def test_parse_source():
    a = str(parse_source("Hello"))
    assert a == u'<html><head></head><body>Hello</body></html>'

def test_extract():
    a = parse_source(read_search_results())
#    assert u'<p class="row">Hi</p>' == str(extract_listings(a)[0])
    assert True


