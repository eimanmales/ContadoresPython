import urllib.request
import sys
from bs4 import BeautifulSoup


datos = urllib.request.urlopen('https://172.16.17.12/hp/device/InternalPages/Index?id=UsagePage')
soup =  BeautifulSoup(datos)
tags = soup('a')
for tag in tags:
	print(tag.get('class'))
