import requests
import time
import random
import json
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
from fake_useragent import UserAgent 

import warnings
warnings.filterwarnings('ignore')



#LlistAlphabet lowercase and uppercase
def listAlphabet(lowercase=True):
    start = ord('a') if lowercase else ord('A')
    end = ord('z') if lowercase else ord('Z')
    return [chr(i) for i in range(start, end + 1)]

#Create random headers
def gen_random_headers():
    list_headers = [
        {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1'}
    ]
    headers = random.choice(list_headers)
    return headers

#Get number's page from website
def get_num_pages(url):
    ua = UserAgent()
    data = requests.get(url, headers = {'User-Agent':'{}'.format(ua.random)})
    print(data)
    soup = BeautifulSoup(data.content, 'html.parser')
    capcha = soup.find("div", {"class": "g-recaptcha"})
    if capcha != None:
        print('CAPCHA FOUND! key is {}'.format(capcha['data-sitekey']))
        body = {"k": '6Lfn_sQZAAAAANYYrihbxzJfLjdild78jHbTGIt5'}
        
        requests.post('https://www.google.com/recaptcha/api2/reload?k={}'.format(capcha['data-sitekey']),headers = {'User-Agent':'{}'.format(ua.random)},  data=json.dumps(body))
        data = requests.get(url, headers = {'User-Agent':'{}'.format(ua.random)})
        soup = BeautifulSoup(data.content, 'html.parser')

    list_num_pages = []
    page = soup.find("a", {"class": "page2"})
    print(page)
    return page.text





