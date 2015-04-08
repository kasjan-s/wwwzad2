__author__ = 'mirtul'


from bs4 import BeautifulSoup
import requests
from urlparse import urljoin
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

wojewodztwa_list = extract_one_level(INDEX_PAGE)
powiaty_list = []
gminy_list = []
gminy = {}
obwody_list = []

for item in wojewodztwa_list:
    item_link = urljoin(MAIN_PAGE, item.get('href'))
    powiaty_list = powiaty_list + extract_one_level(item_link)


for item in powiaty_list:
    item_link = urljoin(MAIN_PAGE, item.get('href'))
    gminy_list = gminy_list + extract_one_level(item_link)

print "Ogarnalem powiaty_list ", len(powiaty_list)
print "Gminy_list maja ", len(gminy_list)

counter_test = 0

for item in gminy_list:
    counter_test += 1
    if counter_test % 100 == 0:
        break

    item_link = urljoin(MAIN_PAGE, item.get('href'))
    additional = extract_one_level(item_link)
    if len(additional) is not 0:
        obwody_list = obwody_list + additional
    else:
        obwody_list = obwody_list + [item]

    print counter_test, len(obwody_list)

print "WSZYSTKO OBWODOW ", len(obwody_list)

counter_test = 0

with open('dane', 'a') as the_file:
    for item in obwody_list:
        counter_test += 1
        if counter_test % 500 == 0:
            print counter_test
#            print "Gonna wait 30 seconds"
#           time.sleep(30)
        item_link = urljoin(MAIN_PAGE, item.get('href'))
        req = None
        while req is None:
            try:
                req = requests.get(item_link, timeout=5)
            except:
                print "byl except"
                req = None
        req.encoding = 'utf-8'
        soup = BeautifulSoup(req.text)
        gmina_field = soup.find(text='Gmina')
        gmina_cell = gmina_field.find_parent()
        gmina_name = gmina_cell.find_next_sibling().text
        print item.text
        print type(item.text)
        the_file.write(item.text.encode('utf-8'))
        the_file.write('\n')
        the_file.write(gmina_name.encode('utf-8'))
        the_file.write('\n')