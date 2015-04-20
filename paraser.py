__author__ = 'mirtul'


from bs4 import BeautifulSoup
import requests
from urlparse import urljoin
from collections import deque
# import time

MAIN_PAGE = 'http://prezydent2010.pkw.gov.pl/PZT/PL/WYN/W/'
INDEX_PAGE = urljoin(MAIN_PAGE, 'index.htm')


def extract_one_level(url):
    r = None
    while r is None:
        try:
            r = requests.get(url, timeout=5)
        except:
            print "byl except"
            r = None
    r.encoding = 'utf-8'
    soups = BeautifulSoup(r.text)
    return soups.select(".col5 > .link1")
'''
wojewodztwa_list = extract_one_level(INDEX_PAGE)
powiaty_list = []
gminy_list = []
gminy = {}
obwody_list = []
'''
extract_list = deque()
extract_list.extend(extract_one_level(INDEX_PAGE))
obwod_list = []


counter_test = 0

while extract_list:
    item = extract_list.popleft()
    counter_test += 1
    if counter_test % 100 == 0:
        print counter_test
    item_link = urljoin(MAIN_PAGE, item.get('href'))
    additional = extract_one_level(item_link)
    if len(additional) is not 0:
        extract_list.extend(additional)
    else:
        obwod_list = obwod_list + [item]

print len(obwod_list)

with open('dane', 'a') as the_file:
    for item in obwod_list:
        item_link = urljoin(MAIN_PAGE, item.get('href'))
        req = None
        while req is None:
            try:
                req = requests.get(item_link, timeout=5)
            except:
                req = None
        req.encoding = 'utf-8'
        soup = BeautifulSoup(req.text)
        gmina_name = soup.find(text='Gmina').find_parent().find_next_sibling().text
        the_file.write(item.text.encode('utf-8'))
        the_file.write('\n')
        the_file.write(gmina_name.encode('utf-8'))
        the_file.write('\n')
