#!/usr/bin/python
# -*- coding: utf-8 -*-
from apscheduler.schedulers.blocking import BlockingScheduler
from bs4 import BeautifulSoup as bs
import requests
import re
import timeit
import datetime
import threading
import sys
from getconf import *
from harvester import harvest_tokens_manually
from add_and_checkout import *

# TO DO: scrape for early links
class bot:
    # Constants
    base_url = 'http://www.supremenewyork.com'

    # Inputs

    number_items_to_buy = 1

    drop_time = [2018, 2, 23, 20, 28, 59]

    found = False

    proxies = [
         {'http': '207.144.127.122:3128'},{'https':'12.221.240.25:8080'}
    ]

    # early_link = 'http://www.supremenewyork.com/shop/jackets/nzpacvjtk' #sold out
    # early_link = 'http://www.supremenewyork.com/shop/jackets/vn2t1jhs3' # mult sizes
    # early_link = 'http://www.supremenewyork.com/shop/accessories/kcgevis8r/xiot9byq4' #one size

    # Functions
    def product_page(self, url, result):
        print('Finding matching products...')
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/52.0.2743.116 Safari/537.36',
            'X-XHR-Referer': 'http://www.supremenewyork.com/shop/all',
            'Referer': 'http://www.supremenewyork.com/shop/all/bags',
            'Accept': 'text/html, application/xhtml+xml, application/xml',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8,da;q=0.6',
            'DNT': '1'
        })

        response = session.get(str(self.base_url) + str(url))
        soup = bs(response.text, 'html.parser')

        h1 = soup.find('h1', {'itemprop': 'name'})

        p = soup.find('p', {'itemprop': 'model'})

        match = []

        if h1 is not None and p is not None:
            model = h1.string.encode('ascii', errors='ignore')
            style = p.string.encode('ascii', errors='ignore')

            for keyword in keywords_model:
                if keyword.title() in model:
                    match.append(1)
                else:
                    match.append(0)

            # add to cart
            if 0 not in match:
                match = []
                for keyword in keywords_style:
                    if keyword.title() in style:
                        match.append(1)
                    else:
                        match.append(0)

                if 0 not in match:
                    print('FOUND: ' + model + ' at ' + self.base_url + url)
                    result[0] = url
                else:
                    sys.exit('Sorry, couldnt find {} in {}'.format(model, style))


    def start_checkout(self, soup, url, parent):
        print"checkout"
        threads = []
        started_threads = []
        results = []
        num_bought = 0
        check = threading.Thread(target=self.check_bought, args=(results, parent))
        check.setDaemon(False)
        check.start()
        for proxy in self.proxies:
            t = Checkout(soup, self.base_url, self.base_url + url, proxy, size, keywords_style[0],
                         self.number_items_to_buy, results, parent)
            threads.append(t)
            print("proxy")
        for t in threads:
            t.start()

    def check_bought(self, results, parent):
        while (True):
            total = 0
            for t in results:
                total += t
                if total >= self.number_items_to_buy:
                    print(total)
                    parent.kill()
                    return

    def on_time(self):
        # Main
        print(datetime.datetime.now())
        start = timeit.default_timer()

    if __name__ == '__main__':
        harvest_tokens_manually()
        on_time()
