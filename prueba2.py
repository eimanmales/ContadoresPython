import requests
import urllib.request as request
from urllib3.exceptions import InsecureRequestWarning
import ssl
import certifi


requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

try:
    site = requests.get(url='https://172.16.17.12/hp/device/InternalPages/Index?id=UsagePage', data={'bar': 'baz'}, verify=False).text
    print(site)
    print("Connection made successfully")

except requests.exceptions.SSLError:
    print("Expired Certificate")