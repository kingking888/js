# -*- coding: utf-8 -*-
# @author   : yuchangqing
# @date     : 2021/4/7
# @File     : sinopec.py
# @Software : PyCharm
import requests
from lxml import etree
import json

url = 'https://bidding.sinopec.com/tpfront/xxgg/004001/'

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
}

session = requests.session()
session.headers = headers

response = session.get(url)
base_url = 'https://bidding.sinopec.com/tpfront/CommonPages/searchmore.aspx?'
res = session.get(base_url, params={"CategoryNum": "004001"})
html = etree.HTML(res.text)
__VIEWSTATE = html.xpath("//input[@id='__VIEWSTATE']/@value")[0]
__VIEWSTATEGENERATOR = html.xpath("//input[@id='__VIEWSTATEGENERATOR']/@value")[0]
__EVENTTARGET = html.xpath("//input[@id='__EVENTTARGET']/@value")[0]
__EVENTARGUMENT = '1'
__VIEWSTATEENCRYPTED = html.xpath("//input[@id='__VIEWSTATEENCRYPTED']/@value")[0]
__EVENTVALIDATION = html.xpath("//input[@id='__EVENTVALIDATION']/@value")[0]
__EVENTTARGET = "MoreinfoListsearch1$Pager"

data = {
    "MoreinfoListsearch1$txtTitle": '',
    "MoreinfoListsearch1$slrq": '',
    "MoreinfoListsearch1$slrq2": '',
    "MoreinfoListsearch1$Pager_input": "1",
    "__EVENTVALIDATION": __EVENTVALIDATION,
    "__VIEWSTATEENCRYPTED": __VIEWSTATEENCRYPTED,
    "__EVENTARGUMENT": __EVENTARGUMENT,
    "__EVENTTARGET": __EVENTTARGET,
    "__VIEWSTATEGENERATOR": __VIEWSTATEGENERATOR,
    "__VIEWSTATE": __VIEWSTATE
}
res = session.post(base_url, params={"CategoryNum": "004001"}, data=json.dumps(data))
print(res.text)
