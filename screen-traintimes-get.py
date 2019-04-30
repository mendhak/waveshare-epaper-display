#! /usr/bin/env python

import os
from bs4 import BeautifulSoup
import requests
import unicodedata
import codecs
import sys

template = 'screen-output-weather.svg'

if sys.argv[1] == "hide":
    print("Hiding train times")
    output = codecs.open(template , 'r', encoding='utf-8').read()
    output = output.replace('TRAIN_DISPLAY_VALUE', "none")
    codecs.open('screen-output-weather.svg', 'w', encoding='utf-8').write(output)
    sys.exit(0)



url = "http://ojp.nationalrail.co.uk/service/ldbboard/dep/SUO/LBG/To"

headers = {
  "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0"
}
response1 = requests.get(url, headers=headers).text

soup = BeautifulSoup(response1,"html.parser")
row = soup.select('table tbody tr td')
train_one_summary = row[0].get_text().strip() + " " + unicodedata.normalize("NFKD", row[1].get_text().strip())[0:9] + " " + row[2].get_text().strip()
print(train_one_summary)

url = "http://ojp.nationalrail.co.uk/service/ldbboard/dep/SUO/ZFD/To"

headers = {
  "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0"
}
response2 = requests.get(url, headers=headers).text

soup = BeautifulSoup(response2,"html.parser")
row = soup.select('table tbody tr td')
train_two_summary =  row[0].get_text().strip() + " " + unicodedata.normalize("NFKD", row[1].get_text().strip())[0:9] + " " + unicodedata.normalize("NFKD", row[2].get_text().strip())


print(train_two_summary)
output = codecs.open(template , 'r', encoding='utf-8').read()
#output = output.replace('ICON_ONE',icon_dict[icon_one])
output = output.replace('TRAIN_ONE_SUMMARY', train_one_summary)
output = output.replace('TRAIN_TWO_SUMMARY', train_two_summary)
codecs.open(template, 'w', encoding='utf-8').write(output)

