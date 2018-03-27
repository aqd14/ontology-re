'''
Scrape features from Firefox releases notes
'''

import requests
from bs4 import BeautifulSoup
from lxml import etree
import re

root = etree.Element('root')
etree.SubElement(root, "system").text = 'Firefox'

for i in range(28, 60):
    release_e = etree.SubElement(root, 'release')
    version = str(i) + '.0'
    release_e.text = version
    features_e = etree.SubElement(release_e, 'features')

    url = 'https://www.mozilla.org/en-US/firefox/' + version + '/releasenotes/'
    result = requests.get(url)
    soup = BeautifulSoup(result.content, 'lxml')
    print(url)
    features = soup.find(id='new-features').find(id='new').find_all(id=re.compile('^note-\d+$'))
    for feature in features:
        etree.SubElement(features_e, "feature").text = feature.find('p').text

    tree = etree.ElementTree(element=root)
    tree.write('firefox-features.xml', pretty_print=True, xml_declaration=True, encoding='utf-8')
