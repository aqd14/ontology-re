'''
Scrape features from Google Chrome  releases notes
'''

'''
Scrape features from Firefox releases notes
'''

import requests
from bs4 import BeautifulSoup
from lxml import etree
import re

root = etree.Element('root')
etree.SubElement(root, "system").text = 'Google Chrome'

for i in range(1, 66):
    release_e = etree.SubElement(root, 'release')
    version = str(i)
    release_e.text = version
    features_e = etree.SubElement(release_e, 'features')

    url = 'https://www.chromestatus.com/features#milestone=' + version
    result = requests.get(url)
    soup = BeautifulSoup(result.content, 'lxml')
    print(url)
    features = soup.find(id='featurelist').find_all(id=re.compile('^\d+$'))
    for feature in features:
        feature_e = etree.SubElement(features_e, 'feature')
        etree.SubElement(feature_e, 'category').text = feature.find(class_='category').text
        etree.SubElement(feature_e, 'title').text = feature.h2.string
        etree.SubElement(feature_e, 'description').text = feature.find(class_='category').summary.span.text

    tree = etree.ElementTree(element=root)
    tree.write('firefox-features.xml', pretty_print=True, xml_declaration=True, encoding='utf-8')
