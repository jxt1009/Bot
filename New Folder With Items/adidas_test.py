import requests
import urllib
import json
from bs4 import BeautifulSoup as bs
import lxml
def URLGen(model, size):
    BaseSize = 580
    # Base Size is for Shoe Size 6.5
    ShoeSize = size - 6.5
    ShoeSize = ShoeSize * 20
    RawSize = ShoeSize + BaseSize
    ShoeSizeCode = int(RawSize)
    URL = 'https://www.adidas.com/us/' + str(model) + '.html?forceSelSize=' + str(model) + '_' + str(ShoeSizeCode)
    return URL

headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/52.0.2743.116 Safari/537.36',
        'DNT': '1',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8,da;q=0.6',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

pid = "CQ3024"
url = URLGen(pid,12)

from selenium import webdriver
driver = webdriver.PhantomJS()
driver.get(url)
p_element = driver.find_element_by_id(id_='defaultOption')
print(p_element.text)

session = requests.session()
response = session.get(url, headers=headers)
soup = bs(response.text, "lxml")
print(soup.text)

